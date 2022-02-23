import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from users.models import Borrower,Payments
from accounts.forms import AddUserForm
from librarysystem.filters import BookFilter
from .models import Book,BookRequests
from .forms import AddBookForm

@login_required
def index(request):
    all_books = Book.objects.all()
    myFilter = BookFilter(request.GET,queryset=all_books)
    all_books = myFilter.qs
    myRequests = BookRequests.objects.filter(request_approval_status='p').count()
    context = {
        'all_books':all_books,
        'myFilter':myFilter,
        'myRequests':myRequests,
    }
    return render(request, 'manager/dashboard.html',context=context)

@login_required
def user_list(request):
    all_users = User.objects.all()
    myRequests = BookRequests.objects.filter(request_approval_status='p').count()
    context = {
        'all_users':all_users,
        'myRequests':myRequests,
    }
    return render(request, 'manager/userboard.html',context=context)

@login_required
def loan_list(request):
    all_loans = Borrower.objects.all()
    myRequests = BookRequests.objects.filter(request_approval_status='p').count()
    context = {
        'all_loans':all_loans,
        'myRequests':myRequests,
    }
    return render(request, 'manager/bookloan.html',context=context)

@login_required
def add_book(request):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Added Succesfully')
            return redirect('manager:index')
        else:
            messages.error(request,"Unable to Add Book")
            return redirect('manager:index')
    else:
        form = AddBookForm()
        return render(request,'manager/addbook.html',{'form':form})

@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Added Succesfully')
            return redirect('manager:user_list')
        else:
            messages.error(request,"Unable to Add User")
            return redirect('manager:user_list')
    else:
        form = AddUserForm()
        return render(request,'manager/adduser.html',{'form':form})

@login_required
def update_book(request,pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    bookobj = Book.objects.get(book_isbn=pk)
    form = AddBookForm(instance=bookobj)
    if request.method == 'POST':
        form = AddBookForm(data=request.POST,instance=bookobj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request,'Book Updated Succesfully')
            return redirect('manager:index')
        else:
            messages.error(request,"Unable to Update Book")
            return redirect('manager:index')
    else:
        return render(request,'manager/updatebook.html',{'form':form})

@login_required
def update_user(request,pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    userobj = User.objects.get(id=pk)
    form = AddUserForm(instance=userobj)
    if request.method == 'POST':
        form = AddUserForm(data=request.POST,instance=userobj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request,'User Updated Succesfully')
            return redirect('manager:user_list')
        else:
            messages.error(request,"Unable to Update User")
            return redirect('manager:user_list')
    else:
        return render(request,'manager/updateuser.html',{'form':form})

@login_required
def delete_book(request, pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    bookobj = Book.objects.get(book_isbn=pk)
    context = {'book':bookobj}
    if request.method == 'POST':
        bookobj.delete()
        messages.success(request,f'{bookobj.book_title} Removed Succesfully')
        return redirect('manager:index')
    else:
        return render(request,'manager/deletebook.html',context=context)


@login_required
def delete_user(request, pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    userobj = User.objects.get(id=pk)
    context = {'userobj':userobj}
    if request.method == 'POST':
        userobj.delete()
        messages.success(request,f'{userobj.first_name} Removed Succesfully')
        return redirect('manager:user_list')
    else:
        return render(request,'manager/deleteuser.html',context=context)



@login_required
def book_requests(request):
    all_requests = BookRequests.objects.filter(request_approval_status='p')
    myRequests = BookRequests.objects.filter(request_approval_status='p').count()
    context = {'all_requests':all_requests,
                'myRequests':myRequests
            }
    return render(request, 'manager/bookrequests.html',context=context)

@login_required
def approve_book_request(request,pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    if request.user.is_authenticated:
        userreq = get_object_or_404(BookRequests,pk=pk)
        approver = get_object_or_404(User,id=str(request.user.id))
        if userreq.user_id.total_book_due < 10:
            a = Borrower()
            a.user_id = userreq.user_id
            a.book_isbn = userreq.book_isbn
            a.borrowed_from_date = datetime.datetime.now()
            a.borrowed_to_date = a.borrowed_from_date + datetime.timedelta(days=5)
            a.issued_by = approver 
            a.save()
            userreq.book_isbn.book_available_copies = userreq.book_isbn.book_available_copies - 1
            userreq.book_isbn.save()
            userreq.user_id.total_book_due=userreq.user_id.total_book_due+1
            userreq.user_id.save()
            userreq.request_approval_status = 'a'
            userreq.save()
            template = render_to_string('manager/email_template.html',{'user':userreq.user_id.first_name,'book':userreq.book_isbn.book_title,'return_date':a.borrowed_to_date})
            email = EmailMessage(
                'Request Approved',
                template,
                settings.EMAIL_HOST_USER,
                [userreq.user_id.email],
            )       
            email.fail_silently = False 
            # email.send()
            messages.success(request,'Book Request Approved')
            return redirect('manager:book_requests')
        else:
            userreq.request_approval_status = 'd'
            messages.error(request,'Book Request Denied, Member has Exceeded Limits')
        return render(request, 'manager/bookrequests.html')
    else:
        return redirect('accounts:login')


@login_required
def return_book(request, pk):
    if not request.user.is_superuser:
        return redirect('frontend:index')
    if request.user.is_authenticated:
        obj = Borrower.objects.get(pk=pk)
        book_pk=obj.book_isbn
        user_pk=obj.user_id
        user = User.objects.get(id=user_pk.id)
        user.total_book_due=user.total_book_due-1
        user.save()
        book=Book.objects.get(book_isbn=book_pk.book_isbn)
        book.book_available_copies=book.book_available_copies+1
        book.save()
        obj.delete()
        messages.success(request,'Book Returned Succesfully')
        return redirect('manager:loan_list')
    else:
        return redirect('accounts:login')
