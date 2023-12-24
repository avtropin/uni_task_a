from time import sleep

from celery import Celery

CELERY_RESPONSE = "Hello World!"

celery = Celery(__name__,
                broker='redis://localhost:6379',
                backend='redis://localhost:6379')


@celery.task
def processing_request(data):
    hw_string = ""
    for sym in CELERY_RESPONSE:
        hw_string += sym
        sleep(1)
    return {"hw_string": hw_string}
