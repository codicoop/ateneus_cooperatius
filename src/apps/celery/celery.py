import os
from datetime import datetime, timedelta

from celery import Celery

from celery.schedules import crontab
from django.apps import apps
from django.conf import settings

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
        notify_activity_organizer.s(),
    )


@app.task
def test(arg):
    print(arg)


@app.task
def notify_activity_organizer():
    activity_model = apps.get_model("cc_courses", "Activity")
    day = datetime.today() + timedelta(
        days=settings.REMIND_SESSION_ORGANIZER_DAYS_BEFORE
    )
    print(f"{day=}")

    activities = activity_model.objects.filter(
        responsible__isnull=False,
        organizer_reminded__isnull=True,
        date_start=day,
    )
    for activity in activities:
        activity.send_reminder_to_responsible()

    print(f"Notifications to responsibles for {len(activities)} sent.")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
