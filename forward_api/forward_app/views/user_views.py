from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from rest_framework import status
from .meta import *
from forward_app.utils.score_system import *


class Signup(APIView, Meta):

    def delete(self, request):
        if request.user.is_staff:
            username, password = request.data["username"], request.data["password"]
            user = User.objects.get(username=username, password=password)
            user.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        # return Response("Sorry. We are not accepting new user signups right now.", status=status.HTTP_204_NO_CONTENT)
        if set(request.data.keys()) == {"username", "email", "password", "first_name", "last_name"}:
            sz = UserSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                sz.save()
                user = User.objects.get(**sz.data)
                persona = Persona(user=user)
                persona.stage = 1
                persona.save()
                return Response(sz.data, status=status.HTTP_201_CREATED)
        return Response("Please provide username, email, password, first name and last name.", status=status.HTTP_400_BAD_REQUEST)


class Login(APIView, Meta):
    def post(self, request):
        username, password = request.data["username"], request.data["password"]
        # if username not in settings.INTERNAL_USERNAMES or password not in settings.INTERNAL_PASSWORDS:
        #     return Response("Please login with internal username and password.",
        #                     status=status.HTTP_401_UNAUTHORIZED)
        exists = User.objects.filter(username=username, password=password).exists()
        if exists:
            user = User.objects.get(username=username, password=password)
            update_scores(pers=Persona.objects.all(), comments=Comment.objects.all())
            sweep(Persona.objects.all())
            sz = UserSerializer(user)
            try:
                persona = user.persona
                pol = persona.politician
                approved = pol.approved
                data = sz.data
                data['approved'] = approved
                data['politician_id'] = pol.id
                return Response(data, status=status.HTTP_202_ACCEPTED)
            except AttributeError:
                data = sz.data
                data['is_mod'] = (persona.stage == 2)
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Users(APIView, Meta):
    permission_classes = [IsAdminUser]

    def get(self, request):
        if set(request.GET.keys()) == {"user_id"}:
            user = User.objects.get(id=int(request.GET["user_id"]))
            sz = ProfileSerializer(user.persona)
            return Response(sz.data, status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            sz = UsernameSerializer(users, many=True)
            return Response(sz.data, status=status.HTTP_200_OK)