from huey import crontab
from huey.contrib.djhuey import task, db_periodic_task, HUEY as huey
from . import predict

@db_periodic_task(crontab(minute='*/10'))
def s():
    print('hello')