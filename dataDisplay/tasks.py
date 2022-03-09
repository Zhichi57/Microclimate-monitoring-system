from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime


@shared_task(name="print_msg_main")
def print_message(message, *args, **kwargs):
    print(f"Celery is working!! Message is {message}")
