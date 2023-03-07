from huey import crontab
from huey.contrib.djhuey import task, db_periodic_task, HUEY as huey
from .models import *
from .predict import *
import json


@db_periodic_task(crontab(minute='*/1'))
def learing_models():
    allusers = User.objects.all()

    for usr in allusers:
        predict_day = []
        predict_month = []
        spending_category_list = []
        myuser_categories = []
        myuser_spendings = spendings.objects.filter(user = usr).order_by('date').values()
        # get all spending category
        for spending in myuser_spendings:
            spending_category_list.append(spending['category_id'])
        # transfer to unique category id
        myuser_categories = list(set(spending_category_list))
        if MyUser.objects.filter(user=usr).exists():
            temp = MyUser.objects.get(user=usr) 
            # temp.prediction["day_prediction"] = 1
            # temp.save()
        else:
            temp = MyUser.objects.create(user=usr) 

        # if not myuser_spendings:
        #     print(usr, "no spendings")
            
        # else:
        #     predict_day, predict_month = predict(list(myuser_spendings))
        #     temp.prediction["day_prediction"] = json.dumps(predict_day, skipkeys=True)
        #     temp.prediction["month_prediction"] = json.dumps(predict_month, skipkeys=True)
        #     temp.save()
        #     print(predict_day)
        #     print(predict_month)
        temp2 = temp.prediction["day_prediction"]

        print(temp2, list(temp2), type(temp2))
        # print(temp.prediction["day_prediction"])
        # print(type(temp.prediction["day_prediction"]))