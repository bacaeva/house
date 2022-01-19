import os
from celery import Celery

from market_api import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_api.settings')
app = Celery('market_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)


@app.task
def add(x,y):
    return x/y
