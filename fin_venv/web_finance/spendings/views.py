from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy


def spendigs_view(request, id):
    myuser = User.objects.get(id=id)
    myuserspendings = spendings.objects.filter(user=myuser).order_by('-date').values()
    allcategories = categories.objects.all().values()
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories': allcategories
    }
    return render(request, 'spendings/list_spendings.html', context)


def add_spending(request):
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            print('form valid', request.POST)
            form.save()
            return redirect('spendings',request.user.id)
        else:
            print('form invalid', request.POST)
    else:
        form = SpendingForm(initial={'user': f'{request.user.id}'})

    context = {
        'form': form,
    }
    return render(request, 'spendings/add_spending.html', context)


def editspending(request, id):
    myspending = spendings.objects.get(id = id)
    form = SpendingForm(request.POST or None, instance=myspending)
    if form.is_valid():
        form.save()
        return redirect('spendings',request.user.id)
        
    context = {
        'form': form,
        'myspending': myspending,
    }
    return render(request, 'spendings/edit_spending.html', context)


def deletespending(request, id):
    pass
    # model = spendings
    # template_name = 'spendings/delete_spending.html'
    # success_url = '/../..'
