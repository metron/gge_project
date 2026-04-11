import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Читаем конфиг из settings.py, префикс CELERY_ означает настройки для селери
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи (tasks.py) во всех приложениях
app.autodiscover_tasks()
