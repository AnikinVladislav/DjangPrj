from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .predict import *
from datetime import datetime
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
import csv
from django.core.paginator import Paginator
from django.db.models import Q


def spendigs_view(request, id):
    myuser = User.objects.get(id=id)
    allcategories = categories.objects.all().order_by('description').values()
    searched_id = []
    query = ''
    print(request.GET)
    # exception with the first opening spendings page
    if ('q' in request.GET):
        query = request.GET['q']
        for cat in allcategories: 
            if request.GET['q'].lower() in cat['description'].lower():
                searched_id.append(cat['id'])
        myuserspendings = spendings.objects.filter(Q(user=myuser) & Q(category__in=searched_id)).order_by('-date').values()
        # set up paginator, 6 spendings per page
        p = Paginator(spendings.objects.filter(Q(user=myuser) & Q(category__in=searched_id)).order_by('-date').values(), 6)
    else:
        myuserspendings = spendings.objects.filter(user=myuser).order_by('-date').values()
        # set up paginator, 6 spendings per page
        p = Paginator(spendings.objects.filter(user=myuser).order_by('-date').values(), 6)



    page = request.GET.get('page')
    spendings_page = p.get_page(page)
    nums = "a" * spendings_page.paginator.num_pages
    nums_ge_6 = spendings_page.paginator.num_pages > 6
    last_num_page = spendings_page.paginator.num_pages
    prelast_num_page = spendings_page.paginator.num_pages - 1
    preprelast_num_page = spendings_page.paginator.num_pages - 2
    
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories': allcategories,
        'spendings_page': spendings_page,
        'nums': nums,
        'nums_ge_6': nums_ge_6,
        'last_num_page': last_num_page,
        'prelast_num_page': prelast_num_page,
        'preprelast_num_page': preprelast_num_page,
        'query': query
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
    print(request.GET)
    if form.is_valid():
        form.save()
        return redirect('spendings',request.user.id)
        
    context = {
        'form': form,
        'myspending': myspending,
    }
    return render(request, 'spendings/edit_spending.html', context)


def deletespending(request, id):
    myspending = spendings.objects.get(id = id)
    myspending.delete()
    messages.success(request, ("Spending was deleted"))
    return redirect('spendings',request.user.id)


def spendingscsv(request):
    responce = HttpResponse(content_type='text/csv')
    responce['Content-Disposition'] = 'attachment; filename=spendings.csv'

    writer = csv.writer(responce)

    myuserspendings = spendings.objects.filter(user = request.user.id).values()
    allcategories = categories.objects.all().order_by('description').values()

    writer.writerow(['id', 'date', 'amount', 'category', 'user'])

    for spending in myuserspendings:
        print(spending)
        cat_id = spending['category_id'] - 1 
        writer.writerow([spending['id'], spending['date'], spending['amount'], allcategories[cat_id]['description'], request.user])

    return responce

def add_category(request):
    allcategories = categories.objects.all().order_by('description').values()
    bad = False
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        for cat in allcategories: 
            if request.POST['description'].lower() == cat['description'].lower():
                bad = True
        if form.is_valid() and not bad:
            print('form valid', request.POST)
            form.save()
            return redirect('add_spending')
        else:
            if bad:
                messages.success(request, ("Category alredy exist"))
            print('form invalid', request.POST)
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'allcategories': allcategories
    }
    return render(request, 'spendings/add_category.html', context)


def charts_spendings(request):
    date = []
    amount_by_date = []
    amount_by_caregory = []
    category_desc = []
    dict_cat = {}
    sel_month = datetime.now().month
    sel_year = datetime.now().year
    list_myuserspendings = []


    myuserspendings = spendings.objects.filter(user = request.user.id).order_by('date').values()
    allcategories = categories.objects.all().values()

    for spending in myuserspendings:
        list_myuserspendings.append(spending)

    for cat in allcategories:
        dict_cat[cat['id']] = [cat['description'], 0]

    if 'sel_month' in request.GET:
        sel_month = int(request.GET['sel_month'])

    if 'sel_year' in request.GET:
        sel_year = int(request.GET['sel_year'])

    for spending in myuserspendings:
        if (spending['date'].month == sel_month or sel_month == 0) and spending['date'].year == sel_year: 
            # exception for 20.012.2023 20.011.2023 20.010.2023 -> 20.12.2023 20.11.2023 20.10.2023
            if spending['date'].month < 10:
                if date == []:
                    date.append(f'{spending["date"].day}.0{spending["date"].month}.{spending["date"].year}')
                    amount_by_date.append(spending["amount"])
                elif date[-1] == f'{spending["date"].day}.0{spending["date"].month}.{spending["date"].year}':
                    amount_by_date[-1] += spending["amount"]
                else:
                    date.append(f'{spending["date"].day}.0{spending["date"].month}.{spending["date"].year}')
                    amount_by_date.append(spending["amount"])
            else:
                if date == []:
                    date.append(f'{spending["date"].day}.{spending["date"].month}.{spending["date"].year}')
                    amount_by_date.append(spending["amount"])
                elif date[-1] == f'{spending["date"].day}.{spending["date"].month}.{spending["date"].year}':
                    amount_by_date[-1] += spending["amount"]
                else:
                    date.append(f'{spending["date"].day}.{spending["date"].month}.{spending["date"].year}')
                    amount_by_date.append(spending["amount"])

            dict_cat[spending['category_id']][1] += spending['amount']
            
    for i in range(1,len(dict_cat)+1):
        category_desc.append(dict_cat[i][0])
        amount_by_caregory.append(dict_cat[i][1])
    

    context = {
        'date': date,
        'amount_by_date': amount_by_date,
        'amount_by_caregory': amount_by_caregory,
        'category_desc': category_desc,
        'sel_month': sel_month,
        'sel_year': sel_year
    }
    return render(request, 'spendings/charts.html', context)


def prediction(request):

    predict_day = []
    predict_month = []
    category_desc = []

    if MyUser.objects.filter(user=request.user.id).exists():
        temp = MyUser.objects.get(user=request.user.id)
        predict_day = temp.prediction["day_prediction"]
        predict_month = temp.prediction["month_prediction"]
        category_desc = temp.prediction["categories"]
 
    context = {
        'category_desc': category_desc,
        'predict_day': predict_day,
        'predict_month': predict_month
    }
    return render(request, 'spendings/prediction_spending.html', context)


