from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.core_models import Politician
from forward_app.core_models import Policy
from forward_app.serializers import UserSerializer, PoliticianSerializer, PolicySerializer, PolicyDetailedSerializer
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

    def post(self, request, format=None):
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


class Policies(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]

    @staticmethod
    def by_category(request, c_id):
        policies = Policy.objects.filter(category=c_id)
        index = request.data.get('index')
        if index != None and isinstance(index, int):
            if len(policies) > index:
                policy = policies[index]
                sz = PolicySerializer(policy)
                return Response(sz.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        sz = PolicySerializer(policies, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)


    @staticmethod
    def by_id(id):
        policy = Policy.objects.get(id=id)
        if policy:
            sz = PolicySerializer(policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get(self, request, format=None):
        c_id = request.data.get('category_id')
        if c_id != None and isinstance(c_id, int):
            return Policies.by_category(request, c_id)
        id = request.data.get('id')
        if id != None and isinstance(id, int):
            return Policies.by_id(id)
        sz = PolicySerializer(Policy.objects.all(), status=status.HTTP_200_OK)
        return Response(sz.data, status=status.HTTP_200_OK)