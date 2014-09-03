from celery import Celery
from models import *
import easyTileServer.settings
import logging
from layers.config import get_config

celery = Celery('tasks', broker=settings.BROKER_URL)

@celery.task()
def generate_config():
	get_config(force=True)
