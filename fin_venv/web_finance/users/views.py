from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
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
            return redirect('/..')
        else:
            messages.success(request, ("Erorr Logging In, Try Again"))
            return redirect('login')  
    else:
        return render(request, "users/login.html")


class RegisterUser(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy('login')
