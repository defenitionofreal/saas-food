import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')

app = Celery('app')

app.conf.enable_utc = False
app.conf.update(timezone='Europe/Moscow')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'clear_part_numbers_config_day': {
#         'task': 'apps.repository.tasks.clear_temporary_part_numbers_task',
#         'schedule':  crontab(hour=7, minute=30, day_of_week=config_env.clear_data_day)
#     },
# }


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
