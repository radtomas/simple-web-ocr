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


class OCRProcessView(APIView):
    def valid_request_data(self, data):
        error_dict = {}
        for k, v in data.items():
            if v is None:
                error_dict[k] = f"Variable {k} not set"
                continue
            if type(v) is str and not v:
                error_dict[k] = f"Variable {k} is empty string"
        return error_dict

    def post(self, request, format=None):
        error_dict = self.valid_request_data(request.data)
        if error_dict:
            return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)

        sig = signature('image.tasks.process_image_task', args=[{
            'url': request.data.get('url'),
            'language': request.data.get('language'),
            'enforce': request.data.get('enforceProcess')
        }])
        celery_task = sig.apply_async(queue='ocr')
        return Response({'task_id': celery_task.task_id}, status=status.HTTP_200_OK)

    def get(self, request, task_id=None, format=None):
        if not task_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        res = AsyncResult(task_id, app=app)
        if res.state == 'SUCCESS':
            return Response({'content': res.get()}, status=status.HTTP_200_OK)
        return Response({'state': res.state}, status=status.HTTP_200_OK)
