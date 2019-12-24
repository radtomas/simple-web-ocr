from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class OCRProcessView(APIView):
    def post(self, request, format=None):
        print('POST')
        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)
