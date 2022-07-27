"""Celery - task manager that helps us to manage and control internal project applications and other commands in SHADOW
MODE. To work with timing delay -> we use crontab (special symbol language), """

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Car_store.settings')

app = Celery('Car_store')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

#============= SCHEDULE ==============

app.conf.beat_schedule = {
    'dealership_test_task_every_10_seconds': {
        'task': 'dealership.tasks.hell',
        'schedule': 10.0,
    },
    'dealership_buy_car_every_30_seconds': {
        'task': 'dealership.tasks.dealership_buy_car',
        'schedule': 30.0,
    }
}