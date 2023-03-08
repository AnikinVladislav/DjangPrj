from huey import crontab
from huey.contrib.djhuey import task, db_periodic_task, HUEY as huey
from .models import *
from .predict import *
import json


@db_periodic_task(crontab(minute='*/30'))
def learing_models():
    allusers = User.objects.all()

    for usr in allusers:
        predict_day = []
        predict_month = []
        spending_category_list = []
        myuser_categories = []
        category_desc = []
        myuser_spendings = spendings.objects.filter(user = usr).order_by('date').values()
        # get all spending category
        for spending in myuser_spendings:
            spending_category_list.append(spending['category_id'])
        # transfer to unique category id
        myuser_categories = list(set(spending_category_list))
        allcategories = categories.objects.all().values()
        for cat in allcategories:
            category_desc.append(cat['description'])

        if MyUser.objects.filter(user=usr).exists():
            temp = MyUser.objects.get(user=usr)
            if not myuser_spendings:
                print(usr, "no spendings")
            else:
                predict_day, predict_month = predict(list(myuser_spendings))
                temp.prediction["day_prediction"] = predict_day
                temp.prediction["month_prediction"] = predict_month
                temp.prediction["categories"] = category_desc
                temp.save() 
        else:
            temp = MyUser.objects.create(user=usr) 

        

