from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TestApi(APIView):
    def get(self, request):
        return Response(data="all good", status=status.HTTP_200_OK)
