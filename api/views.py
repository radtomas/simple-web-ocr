from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ImageSerializer
from ocr.utils import ImageProcess


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

        image_process = ImageProcess(
            request.data.get('url'),
            request.data.get('language'),
            request.data.get('enforce_process')
        )
        serializer = ImageSerializer(image_process.process_image())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
