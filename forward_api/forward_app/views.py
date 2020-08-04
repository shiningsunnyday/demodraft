from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status


class Meta(object):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]


class Signup(APIView, Meta):
    def post(self, request):
        username, email, password = request.data["username"], request.data["email"], request.data["password"]
        user = User.objects.create_user(username, email, password)
        user.save()
        sz = UserSerializer(user)
        return Response(sz.data, status=status.HTTP_201_CREATED)


class Login(APIView, Meta):
    def get(self, request):
        username, password = request.data["username"], request.data["password"]
        user = authenticate(username=username, password=password)
        if user:
            sz = UserSerializer(user)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Users(APIView, Meta):
    def get(self, request):
        users = User.objects.all()
        sz = UserSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)


class Policies(APIView, Meta):
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
    def by_id(id, detailed=False):
        policy = Policy.objects.get(id=id)
        if policy:
            sz = PolicyDetailedSerializer(policy) if detailed else PolicySerializer(policy)
            pop = policy.popularity
            data = sz.data
            data['likes'] = pop.likes
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if set(request.data.keys()) != {"category", "name", "statement", "description"}:
            return Response("Please provide category, name, statement and description.",
                            status=status.HTTP_400_BAD_REQUEST)

        sz = PolicyDetailedSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            policy = Policy.objects.create(**sz.data)
            pop = Popularity.objects.create(policy=policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.data.get('id')
        policy = Policy.objects.get(id=id)
        policy.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        c_id = request.data.get('category_id')
        if c_id != None and isinstance(c_id, int):
            return Policies.by_category(request, c_id)
        id = request.data.get('id')
        if id != None and isinstance(id, int):
            return Policies.by_id(id)
        sz = PolicySerializer(Policy.objects.all(), many=True)

        return Response(sz.data, status=status.HTTP_200_OK)


class PolicyV(APIView, Meta):
    def get(self, request):
        id = request.data.get('id')
        return Policies.by_id(id, detailed=True)

    def put(self, request):
        id = request.data.get('id')
        policy = Policy.objects.get(id=id)
        pop = policy.popularity
        pop.likes += 1
        pop.save()
        sz = PopularitySerializer(pop)
        return Response(sz.data, status=status.HTTP_202_ACCEPTED)