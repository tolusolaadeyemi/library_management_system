import datetime,string,random,json,requests
from datetime import datetime, timezone,tzinfo
from dateutil import parser
from django.utils import timezone
from django.http import Http404,HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from accounts.models import User
from manager.models import Book,BookRequests
from .models import Borrower,Payments

now_aware = datetime.now(timezone.utc)
tz_info = now_aware.tzinfo
@login_required
def homepage(request):
    if request.user.is_authenticated:
        myRequestsct = BookRequests.objects.filter(user_id=request.user).filter(request_approval_status='p').count()
        appRequests = Borrower.objects.filter(user_id=request.user).count()
        myBooks = Borrower.objects.filter(user_id=request.user)
        days_late = None
        currenttime = None
        for i in myBooks:
            a = Borrower()
            currenttime = datetime.now(tz_info)
            a.borrowed_to_date = i.borrowed_to_date
            due_date = a.borrowed_to_date.strftime('%d')
            due_date = int(due_date)
            todays_date = currenttime.strftime('%d') #change to %d
            todays_date = int(todays_date)
            days_late = todays_date - due_date
        return render(request,'users/homepage.html',context={'myRequestsct':myRequestsct,'appRequests':appRequests,'myBooks':myBooks,'days_late':days_late,'currenttime':currenttime})
    else:
        return redirect('accounts:login')

@login_required
def book_detail(request,pk):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(book_isbn=pk)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        return render(request, 'users/book_detail.html', context={'book': book})
    else:
        return redirect('accounts:login')

@login_required
def borrow_book(request,pk):
    if request.user.is_authenticated:
            obj = Book.objects.get(book_isbn=pk)
            bookreq = get_object_or_404(User,id=int(request.user.id))
            if bookreq.total_book_due < 10:
                a = BookRequests()
                a.user_id = bookreq
                a.book_isbn = obj
                a.save()
                messages.success(request,'Book Request recieved, kindly wait for the Librarian to process the request within 24 hours')
                return redirect('users:homepage')
            else:
                messages.error("You have exceeded the Request Limit")
            return render(request, 'users/book_detail.html',context={'book': obj})
    else:
        return redirect('accounts:login')

@login_required()
def pending_requests(request):
    if request.user.is_authenticated:
        myRequests = BookRequests.objects.filter(user_id=request.user, request_approval_status='p')
        myRequestsct = BookRequests.objects.filter(user_id=request.user).filter(request_approval_status='p').count()
        appRequests = Borrower.objects.filter(user_id=request.user).count()
        return render(request,'users/pendingreqs.html',context={'myRequests':myRequests,'myRequestsct':myRequestsct,'appRequests':appRequests})
    else:
        return redirect('accounts:login')

def generate_ref():
    r = random.sample(string.digits,10)
    ref = ''.join(r)
    return ref

@login_required()
def overdue_books(request):
    if request.user.is_authenticated:
        myRequests = BookRequests.objects.filter(user_id=request.user, request_approval_status='p')
        myRequestsct = BookRequests.objects.filter(user_id=request.user).filter(request_approval_status='p').count()
        appRequests = Borrower.objects.filter(user_id=request.user).count()
        a = Borrower()
        currenttime = datetime.now(tz_info)
        all_overdue = Borrower.objects.filter(user_id=request.user).filter(borrowed_to_date__lte=currenttime)
        days_late = None
        late_fees = None
        amtkobo = None
        for i in all_overdue:
            a.borrowed_to_date = i.borrowed_to_date
            due_date = a.borrowed_to_date.strftime('%d')
            due_date = int(due_date)
            todays_date = currenttime.strftime('%d') #change to %d
            todays_date = int(todays_date)
            days_late = todays_date - due_date
            late_fees = 100 * days_late
            amtkobo = float(late_fees) * 100
        return render(request,'users/overduebooks.html',context={'all_overdue':all_overdue,'currenttime':currenttime,'myRequests':myRequests,'myRequestsct':myRequestsct,'appRequests':appRequests,'late_fees':late_fees,'days_late':days_late,'amtkobo':amtkobo})
    else:
        return redirect('accounts:login')

@login_required()
def payment_confirmation(request):
    if request.user.is_authenticated:
        data = Payments.objects.filter(user_id=request.user)
        for i in data:
            trxref = i.payment_id
        headers = {"Content-Type":"application/json","Authorization":"paystack_key","Cache-Control":"no-cache"}
        response = requests.get(f'https://api.paystack.co/transaction/verify/{trxref}',headers=headers)
        rsp = response.json()
        print(rsp)
        if rsp['status'] == True:
            data = Payments.objects.filter(user_id=request.user)
            for i in data:
                i.payment_status = True
            i.save()  
            return render(request,'users/confirmation.html',context={'data':data})
        else:
            messages.error(request,'Confirmation Failed, Please Try Again')
            return redirect('users:overdue_books')
    else:
        return redirect('accounts:login')

@login_required()
def pay_fees(request,pk):
    if request.user.is_authenticated:
            b = Borrower.objects.filter(pk=pk)
            payee = get_object_or_404(User,id=str(request.user.id))
            currenttime = datetime.now(tz_info)
            all_overdue = Borrower.objects.filter(user_id=request.user).filter(borrowed_to_date__lte=currenttime)
            for i in all_overdue:
                b.borrowed_to_date = i.borrowed_to_date
                due_date = b.borrowed_to_date.strftime('%d')
                due_date = int(due_date)
                todays_date = currenttime.strftime('%d') #change to %d
                todays_date = int(todays_date)
                days_late = todays_date - due_date
                late_fees = 100 * days_late
                t = Payments()
                t.payment_id = generate_ref()
                t.user_id = payee
                t.book_isbn = i.book_isbn
                t.late_fees_charged = late_fees
                amtkobo = float(late_fees) * 100
                # t.payment_status = True
                t.save()
                messages.success(request,'Payment Received, Thank you!')
                data = {"ref":t.payment_id,"amount":amtkobo,"email":request.user.email}
            return HttpResponse(json.dumps(data), content_type="applocation/json")
    else:
        return redirect('accounts:login')