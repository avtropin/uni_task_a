from time import sleep

from celery import Celery
from redis import Redis

CELERY_RESPONSE = "Hello World!"

celery = Celery(__name__,
                broker='redis://localhost:6379',
                backend='redis://localhost:6379')


@celery.task(ignore_result=True)
def processing_request(data):
    hw_string = ""
    r = Redis("uni_redis", 6379)
    id_proc = processing_request.request.id
    for sym in (CELERY_RESPONSE + "$"):
        hw_string += sym
        r.set(id_proc, hw_string)
        sleep(1)
