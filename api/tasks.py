from celery import task

from ocr.utils import ImageProcess


@task
def add(x, y):
    return x + y

@task
def process_image_task(payload):
    image_process = ImageProcess(**payload)
    image_process = image_process.process_image()
    return image_process.content
