from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import categories,User,spendings

def web_finance(request):
    template = loader.get_template('web_finance/main_page.html')
    return HttpResponse(template.render())

def all_spendigns(request, id):
    myuser = User.objects.get(id=id)
    myuserspendings = spendings.objects.filter(user=myuser).values()
    allcategories = categories.objects.all().values()
    template = loader.get_template('web_finance/list_spendings.html')
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories' : allcategories
    }
    return HttpResponse(template.render(context, request))

def about_us(request):
    template = loader.get_template('web_finance/info.html')
    return HttpResponse(template.render())