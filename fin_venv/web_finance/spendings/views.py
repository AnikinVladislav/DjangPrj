from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from .forms import *


def spendigs_view(request, id):
    myuser = User.objects.get(id=id)
    myuserspendings = spendings.objects.filter(user=myuser).values()
    allcategories = categories.objects.all().values()
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories': allcategories
    }
    return render(request, 'spendings/list_spendings.html', context)


def add_spending(request):
    submitted = False
    allcategories = categories.objects.all().values()
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy('main')
            submitted = True
        else:
            print('form is not valid')
    else:
        form = SpendingForm

    context = {
        'form': form,
        'submitted': submitted,
        'categories': allcategories
    }
    return render(request, 'spendings/add_spending.html', context)
