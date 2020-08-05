from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *


class Address(APIView, Meta):

    @staticmethod
    def user_exists(username, password=None):
        filtered = User.objects.filter(username=username)
        if password:
            filtered = filtered.filter(password=password)
        return filtered.exists()

    def get(self, request):
        if set(request.data.keys()) != {"username", "password"}:
            return Response("Please provide username and password.", status=status.HTTP_400_BAD_REQUEST)
        username, password = request.data["username"], request.data["password"]
        if Address.user_exists(username, password):
            user = User.objects.get(username=username, password=password)
            persona = user.persona
            address = {}
            address['line1'] = persona.line1
            address['city'] = persona.city
            address['state'] = persona.state
            address['zip'] = persona.zipcode
            return Response(address, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        if set(request.data.keys()) != {"username", "password", "address"}:
            return Response("Please provide username and address.", status=status.HTTP_400_BAD_REQUEST)
        username, password = request.data["username"], request.data["password"]
        if Address.user_exists(username, password):
            user = User.objects.get(username=username, password=password)
            norm_address = normalizeAddress(request.data["address"])
            persona = user.persona
            persona.line1 = norm_address['line1']
            persona.city = norm_address['city']
            persona.state = norm_address['state']
            persona.zipcode = norm_address['zip']
            persona.save()
            positions = fetchPositions(request.data["address"])
            return Response(positions, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if set(request.data.keys()) != {"username", "scope", "index"}:
            return Response("Please provide username, one of local/state/country and index.",
                            status=status.HTTP_400_BAD_REQUEST)
        username = request.data["username"]
        if Address.user_exists(username):
            user = User.objects.get(username=username)
            persona = user.persona
            address = toAddress(persona)
            positions = fetchPositions(address)
            pos = positions[request.data['scope']][request.data['index']]
            sz = UserSerializer(user)
            data = sz.data
            data['position'] = pos['name']
            return Response(data, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

