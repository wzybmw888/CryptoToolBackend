import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
app = Celery("crypto_quant", backend="redis://127.0.0.1:6379/10")

app.config_from_object('config.settings.local')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 启动命令 celery -A api.apps.utils.celery worker  -l info
