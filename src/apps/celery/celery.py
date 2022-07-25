import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

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
    sender.add_periodic_task(10.0, test.s('hello'), name='run every 10 seconds')
    """

    # Executes every day at 5:00 a.m.
    sender.add_periodic_task(
        crontab(hour=5, minute=0),
        # test.s('Happy Mondays!'),
    )


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
