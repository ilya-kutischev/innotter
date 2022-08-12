"""
Celery config file
"""
from __future__ import absolute_import
import os
from time import sleep
from celery import Celery, shared_task
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')
app = Celery("innotter")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.task
@shared_task
def post_created_task(content, page_uuid, reply_to_id):
    from pages.models import Page
    from users.models import User

    page = Page.objects.get(uuid=page_uuid)

    reply_to = User.objects.get(id=reply_to_id)

    recipient_list = page.followers.values('email')
    recipient_list = [email['email'] for email in recipient_list]
    res = send_mail(
        subject=f'{page.name} posted new post! Check it!',
        message=content,
        from_email='innotter@gmail.com',
        recipient_list=recipient_list,
        fail_silently=False,
    )
    sleep(1)
    print(f"Email sent to {res} members")
    return 0