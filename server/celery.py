# server/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Optional - configure periodic tasks
app.conf.beat_schedule = {
    'fetch-erank-data-every-5-minutes': {
        'task': 'erank_app.tasks.fetch_erank_data',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
        'args': ('shop_name',),  # Provide actual shop name
    },
}
