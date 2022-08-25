from celery import Celery
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')
BROKER = os.environ['CELERY_BROKER']
app = Celery("Microservice", broker=BROKER)