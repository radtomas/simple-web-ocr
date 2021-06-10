from celery import task

from image.utils import ImageProcess


@task
def add(x, y):
    return x + y

@task
def process_image_task(context, enforce):
    image_process = ImageProcess(context, enforce)
    result = image_process.process_image()
    return result
