import os

from celery import Celery

# Установить настройки по умолчанию из Django-проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Использование здесь строки означает, что рабочему процессу не нужно сериализовать
# объект конфигурации дочерним процессам.
# - namespace='CELERY' означает, что все ключи конфигурации, связанные с Celery,
# должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружать задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()
