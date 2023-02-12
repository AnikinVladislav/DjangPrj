from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

from .forms import *

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("Erorr Logging In, Try Again"))
            return redirect('login')  
    else:
        return render(request, "users/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logout"))
    return redirect('main')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Account was registrated"))
            return redirect('main')
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html",{
        'form': form,
    })

