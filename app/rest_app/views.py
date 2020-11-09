from django.views.decorators.cache import cache_control
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal
from .utils import csv_parser, get_top_customers


class UploadData(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        result = csv_parser(request.data)

        if result:
            return Response('Файл был обработан без ошибок',
                            status=status.HTTP_200_OK
                            )
        else:
            return Response('Error, Desc:' + str(serializer.errors) +
                            '- в процессе обработки файла произошла ошибка',
                            status=status.HTTP_400_BAD_REQUEST
                            )


class GetData(APIView):

    @cache_control(must_revalidate=True, max_age=3600)
    def get(self, request, format=None):

        result = get_top_customers()

        return Response(result, status=status.HTTP_200_OK)
