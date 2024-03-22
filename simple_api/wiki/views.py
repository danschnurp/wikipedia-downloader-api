
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FirstParagraph(APIView):

    def get(self, request, format=None):
        # todo fetching data from wiki and ensure correctness
        return Response({}, status=status.HTTP_200_OK)

