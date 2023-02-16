from django.shortcuts import render
from django.http import HttpResponseRedirect
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
            return HttpResponseRedirect('/add_spending?submitted=True')
    else:
        form = SpendingForm
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted,
        'categories': allcategories
    }
    return render(request, 'spendings/add_spending.html', context)
