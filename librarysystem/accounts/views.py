from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from .models import User

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {user}!')
            return redirect('frontend:index')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('accounts:signup')
    else:
        form = NewUserForm()
        return render(request,'accounts/signup.html',{'form':form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:check_user')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                print(user.email)
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('accounts:check_user')
            else:
                messages.error(request,"Invalid username or password.")
                return redirect('accounts:login')
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('accounts:login')
    else:
        form = AuthenticationForm()
        return render(request,'accounts/login.html', {'login_form':form})
   
def user_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('frontend:index') 

def check_user(request):
    if request.user.is_superuser == True:
        return redirect('manager:index')
    else:
        return redirect('frontend:index')
