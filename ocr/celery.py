from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocr.settings')

app = Celery('ocr')

app.conf.update(
    result_backend=settings.CELERY_BACKEND,
    broker_url=settings.CELERY_BROKER,
    task_routes={
        'image.tasks.*': {'queue': 'ocr'},
    },
    default_queue='ocr',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    enable_utc=True,
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
