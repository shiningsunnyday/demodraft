from forward_app.utils.civic import fetch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta


class Address(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) != {"address"}:
            return Response("Please provide just address.", status=status.HTTP_400_BAD_REQUEST)
        names = fetch(request.data["address"])
        return Response(names, status=status.HTTP_200_OK)