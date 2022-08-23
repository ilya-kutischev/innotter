"""
Celery config file
"""
from __future__ import absolute_import
import os
from time import sleep
from celery import Celery, shared_task
# from celery.bin.control import inspect
from kombu import Exchange, Queue
import asyncio



from django.core.mail import send_mail
import boto3


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')
app = Celery("innotter", broker="amqp://admin:admin@rabbitmq:5672")


# app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('post_created_task', Exchange('Emails'), routing_key='email_notifications'),
    # queue for microservice
    # Queue('statistics', Exchange('Microservice'), routing_key='statistics'),
)

# AWS sending email
# @app.task(name='post_created_task', queue='post_created_task')
# def post_created_task(content, page_uuid, reply_to_id):
#     ses_client = boto3.client("ses",
#                               region_name="us-west-2",
#                               aws_access_key_id="sus",
#                               aws_secret_access_key="sus",
#                               endpoint_url="http://localstack:4566")
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

# Django sending email
@app.task(name='post_created_task', queue='post_created_task')
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
    sleep(0)
    print(f"Email sent to {res} members")
    return 0


# async def publish(method='', exchange='Microservice', queue='statistics', message='Hello World!'):
#     import aio_pika
#     import json
#     connection = await aio_pika.connect_robust(
#         "amqp://admin:admin@rabbitmq:5672/",
#     )
#     print("connection created")
#     async with connection:
#         routing_key = "statistics"
#
#         channel = await connection.channel()
#         print("channel created")
#         await channel.default_exchange.publish(
#
#             aio_pika.Message(body=f"Hello {routing_key}".encode()),
#             routing_key=routing_key,
#         )
#         print("message published")

#
# def publish(method='', exchange='Microservice', queue='statistics', message='Hello World!'):
#     import pika
#     import json
#     # before start should create such user in rabbit
#     params = pika.URLParameters('amqp://admin:admin@rabbitmq:5672/')
#
#     connection = pika.BlockingConnection(params)
#     channel = connection.channel()
#     channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
#
#     # result = channel.queue_declare(queue='', exclusive=True)
#     # queue_name = result.method.queue
#
#     channel.basic_qos(prefetch_count=1)
#
#     result = channel.queue_declare(queue=queue, exclusive=True, durable=True)
#     queue_name = result.method.queue
#     properties = pika.BasicProperties(content_type='application/json', content_encoding='utf-8', delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
#
#     channel.basic_publish(exchange=exchange,
#                           routing_key=queue,
#                           body=json.dumps(message),
#                           properties=properties)
#     print(f" [admin producer] Sent a message: \n `{message}`")
#
#     channel.close()
