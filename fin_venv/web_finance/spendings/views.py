from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime


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
    submitted = False
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('spendings',request.user.id)
            submitted = True
        else:
            print('form is not valid')
            print(request.POST)
            return redirect('add_spending')
    else:
        allcategories = categories.objects.all().values()
        form = SpendingForm

    context = {
        'form': form,
        'submitted': submitted,
        'categories': allcategories,
    }
    return render(request, 'spendings/add_spending.html', context)
