import os

from celery import Celery

from celery.schedules import crontab
from django.conf import settings
from django.utils import timezone

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

app = Celery("conf")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Given that when using the crontab way of scheduling tasks the minimum rate
    is every minute, during development you might prefer to use this format:
    sender.add_periodic_task(10.0, function_name.s('hello'))
    """

    # Executes every day at settings.DAILY_TASKS_EXECUTION_TIME
    sender.add_periodic_task(
        crontab(hour=settings.DAILY_TASKS_EXECUTION_TIME),
        test.s(
            f"Scheduled task run at {settings.DAILY_TASKS_EXECUTION_TIME}:nn."
        ),
    )


@app.task
def test(arg):
    print(f"hora actual: {timezone.now()}")
    print(arg)


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
