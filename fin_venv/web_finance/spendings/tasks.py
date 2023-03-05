from huey import crontab
from huey.contrib.djhuey import task, db_periodic_task, HUEY as huey
from .models import *
from .predict import *

@db_periodic_task(crontab(minute='*/1'))
def learing_models():
    allusers = User.objects.all()
    # myuser = User.objects.get(id=1)
    # john = MyUser.objects.create(user=myuser)

    # print(john)

    for usr in allusers:
        predict_day = []
        predict_month = []
        spending_category_list = []
        myuser_categories = []
        myuser_spendings = spendings.objects.filter(user = usr).order_by('date').values()
        # get all spending category
        for spending in myuser_spendings:
            spending_category_list.append(spending['category_id'])
        # transfer to unique categoru id
        myuser_categories = list(set(spending_category_list))
        if MyUser.objects.filter(user=usr).exists():
            temp = MyUser.objects.get(user=usr) 
            # temp.prediction["day_prediction"] = 1
            # temp.save()
        else:
            temp = MyUser.objects.create(user=usr) 

        if not myuser_spendings:
            print(usr, "no spendings")
            
        else:
            predict_day, predict_month = predict(list(myuser_spendings))


        print(temp.prediction)