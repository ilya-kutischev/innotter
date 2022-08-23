from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')
app = Celery("Microservice", broker="amqp://admin:admin@rabbitmq:5672")