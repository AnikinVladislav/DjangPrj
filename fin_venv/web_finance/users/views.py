from django.shortcuts import render
from django.views.generic.edit import CreateView
# from django.contrib.auth.forms import UserCreationForm
from .forms import *

# Create your views here.
def login(request):
    return render(request, "users/login.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = "users/login.html"
