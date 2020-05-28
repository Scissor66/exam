import logging
import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam.settings')

celery_app = Celery('exam')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['exam.tasks.subscriber'])

clog = logging.getLogger('celery')

celery_app.conf.beat_schedule = {
    'unhold': {
        'task': 'exam.tasks.subscriber.unhold_task',
        'schedule': crontab(minute='*/10'),
    },
}


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)
