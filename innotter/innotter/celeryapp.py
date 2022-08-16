"""
Celery config file
"""
from __future__ import absolute_import
import os
from time import sleep
from celery import Celery, shared_task
import celery
from celery.bin.control import inspect

from django.core.mail import send_mail
import boto3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')
app = Celery("innotter")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# AWS sending email
#
# @app.task
# def post_created_task(content, page_uuid, reply_to_id):
#     ses_client = boto3.client("ses",
#                               region_name="us-west-2",
#                               aws_access_key_id="sus",
#                               aws_secret_access_key="sus",
#                               endpoint_url="http://localhost:4566")
#     ses_client.verify_email_identity(EmailAddress="innotter@gmail.com")
#     CHARSET = "UTF-8"
#
#     from pages.models import Page
#     from users.models import User
#
#     page = Page.objects.get(uuid=page_uuid)
#     # reply_to = User.objects.get(id=reply_to_id)
#
#     recipient_list = page.followers.values('email')
#     recipient_list = [email['email'] for email in recipient_list]
#
#     response = ses_client.send_email(
#         Destination={
#             "ToAddresses": recipient_list,
#         },
#         Message={
#             "Body": {
#                 "Text": {
#                     "Charset": CHARSET,
#                     "Data": content,
#                 }
#             },
#             "Subject": {
#                 "Charset": CHARSET,
#                 "Data": f'{page.name} posted new post! Check it!',
#             },
#         },
#         Source="innotter@gmail.com",
#     )





# @app.task
# # @shared_task
# def post_created_task(content, page_uuid, reply_to_id):
#     from pages.models import Page
#     from users.models import User
#
#     page = Page.objects.get(uuid=page_uuid)
#
#     reply_to = User.objects.get(id=reply_to_id)
#
#     recipient_list = page.followers.values('email')
#     recipient_list = [email['email'] for email in recipient_list]
#     res = send_mail(
#         subject=f'{page.name} posted new post! Check it!',
#         message=content,
#         from_email='innotter@gmail.com',
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )
#     sleep(1)
#     print(f"Email sent to {res} members")
#     return 0

inspect().stats()
inspect().ping()
# @app.task
@shared_task
def post_created_task(content, page_uuid, reply_to_id):
    ses_client = boto3.client("ses",
                              region_name="us-west-2",
                              aws_access_key_id="sus",
                              aws_secret_access_key="sus",
                              endpoint_url="http://localhost:4566")
    ses_client.verify_email_identity(EmailAddress="innotter@gmail.com")
    CHARSET = "UTF-8"

    # from pages.models import Page
    # from users.models import User

    # page = Page.objects.get(uuid=page_uuid)
    # reply_to = User.objects.get(id=reply_to_id)
    #
    # recipient_list = page.followers.values('email')
    # recipient_list = [email['email'] for email in recipient_list]

    response = ses_client.send_email(
        Destination={
            "ToAddresses": ["kutischev10@gmail.com"],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": content,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": f'f posted new post! Check it!',
            },
        },
        Source="innotter@gmail.com",
    )