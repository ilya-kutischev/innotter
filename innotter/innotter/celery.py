"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
from __future__ import absolute_import
import os
from celery import Celery

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
from django.core.mail import send_mail

from innotter import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')

app = Celery("innotter")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def post_created_task(content, page, reply_to):
    recipient_list = page.followers.values('email')
    recipient_list = [email['email'] for email in recipient_list]
    res = send_mail(
        subject=f'{page.name} posted new post! Check it!',
        message=content,
        from_email='innotter@gmail.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return print(f"Email sent to {res} members")