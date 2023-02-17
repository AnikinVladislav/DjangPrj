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
        if form.is_valid() and float(request.POST['amount']) > 0:
            print(request.POST)
            form.save()
            return redirect('spendings',request.user.id)
        else:
            errors = 'form is not valid'
            if float(request.POST['amount']) <= 0:
                messages.success(request, ("Amount must be a positive value"))
            else:
                messages.success(request, ("Form not correctle filled"))
            print(errors)
            return redirect('add_spending')
    else:
        allcategories = categories.objects.all().values()
        form = SpendingForm

    context = {
        'form': form,
        'categories': allcategories,
    }
    return render(request, 'spendings/add_spending.html', context)


# def edit_spending(request, id):
#     myspending = spendings.objects.get(id=id)
#     form = SpendingForm(request.POST or None, instance=myspending)
#     allcategories = categories.objects.all().values()
#     context = {
#         'form': form,
#         'categories': allcategories,
#     }
#     return render(request, 'spendings/edit_spending.html', context)



class EditSpendingView(generic.UpdateView):
    model = spendings
    template_name = 'spendings/add_spending.html'
    form_class = SpendingForm
    # success_url = reverse_lazy('spendings')

