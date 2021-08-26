
# This will make sure the app is always imported when
# Django strarts so that shared_task will user this app.

from .celery import app as celery_app

__all__ = ('celery_app')