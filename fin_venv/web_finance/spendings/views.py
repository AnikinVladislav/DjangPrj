from django.shortcuts import render
from .models import *

def spendigs_view(request, id):
    myuser = User.objects.get(id=id)
    myuserspendings = spendings.objects.filter(user=myuser).values()
    allcategories = categories.objects.all().values()
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories': allcategories
    }
    return render(request,'spendings/list_spendings.html',  context)


