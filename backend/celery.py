from __future__ import absolute_import, unicode_literals

import logging
import os
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings
import django

logger = logging.getLogger()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.config_from_object('django.conf:settings', namespace='CELERY')


# app.conf.beat_schedule = {
#     'set_statistics-every-60-minutes-contrab': {
#         'task': 'set_statistics',
#         'schedule': crontab(minute='*/30'),
#         'options': {
#             'expires': 300
#         }
#     },
#     'auto_route-every-60-minutes-contrab': {
#         'task': 'generate_auto_route_periodic',
#         'schedule': crontab(minute='*/30'),
#         'options': {
#             'expires': 300
#         }
#     },
#     'notification-every-5-minutes-contrab': {
#         'task': 'notification_schedule',
#         'schedule': crontab(minute='*/5'),
#         'options': {
#             'expires': 300
#         }
#     },
# }

