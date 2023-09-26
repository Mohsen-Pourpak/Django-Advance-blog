import time

from celery import shared_task


@shared_task
def sendEmail():
    time.sleep(5)
    print("Done@!")