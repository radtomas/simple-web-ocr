from time import sleep

from celery import signature
from celery.app.control import Inspect
from celery.result import AsyncResult
from image.tasks import add
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.pagination import StandardResultsSetPagination
from api.serializers import ImageSerializer
from image.models import Image
from ocr.celery import app


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination


class TestTaskRun(APIView):
    def get(self, request, format=None):
        res = add.delay(4, 4)
        while not res.ready():
            print(res.ready())
            sleep(1)
        i = Inspect()
        print(i)
        return Response(status=status.HTTP_200_OK)


class OCRProcessAPIView(APIView):
    def post(self, request, format=None):
        image, created = Image.objects.get_or_create(
            url=request.data.get('url'),
            language=request.data.get('language'),
        )
        sig = signature('image.tasks.process_image_task', args=[
            image.process_context,
            request.data.get('enforceProcess')
        ])
        celery_task = sig.apply_async(queue='ocr')
        image.task_id = celery_task.task_id
        image.save()
        return Response({'id': image.id}, status=status.HTTP_200_OK)

    def get(self, request, image_id=None, format=None):
        if not image_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        image = Image.objects.get(id=image_id)
        res = AsyncResult(image.task_id, app=app)
        if res.state == 'SUCCESS':
            return Response(ImageSerializer(image).data, status=status.HTTP_200_OK)
        return Response({'state': res.state}, status=status.HTTP_200_OK)
