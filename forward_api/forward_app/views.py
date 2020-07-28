from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.core_models import Politician
from forward_app.serializers import UserSerializer, PoliticianSerializer
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows politicians to be viewed or edited.
    """
    # authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PoliticianViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows politicians to be viewed or edited.
    """
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer


# @api_view(['POST'])
# def sign_up(request):
#     """
#     API endpoint that receives POST requests
#     """
#     if request.method == 'POST':
#         sz = UserSerializer(data=request.data)
#         if sz.is_valid():
#             sz.save()
#             return Response(status=status.HTTP_201_CREATED)

class Signup(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]

    def create(self, request, format=None):
        username, email, password = request.data["username"], request.data["email"], request.data["password"]
        user = User.objects.create_user(username, email, password)
        user.save()
        sz = UserSerializer(user)
        return Response(sz.data, status=status.HTTP_201_CREATED)


class Login(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        username, password = request.data["username"], request.data["password"]
        user = authenticate(username=username, password=password)
        if user:
            sz = UserSerializer(user)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

