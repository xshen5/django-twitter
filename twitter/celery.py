
import os

from celery import Celery

# set the defuatl Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')

app = Celery('twitter')

app.config_from_object('django.conf:settings', namespace='CELERY')

# load task modules from all reigster django app configs
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')