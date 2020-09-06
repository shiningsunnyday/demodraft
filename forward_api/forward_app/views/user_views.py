from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from forward_app.serializers import *
from rest_framework import status
from .meta import *
from forward_app.utils.score_system import *
from django.contrib.auth import authenticate


class Signup(APIView, Meta):
    permission_classes = (AllowAny,)

    def delete(self, request):
        if request.user.is_staff:
            username, password = request.data["username"], request.data["password"]
            user = User.objects.get(username=username, password=password)
            user.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if set(request.data.keys()) == {"username", "email", "password", "first_name", "last_name"}:
            sz = UserSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                email = request.data["email"]
                # A user is creatable only if request's user is a staff user or email is on approved contact list
                # if not request.user.is_staff and not search(email, "./forward_app/utils/contact_list.txt"):
                #     return Response(status=status.HTTP_403_FORBIDDEN)
                sz.save()
                user = User.objects.get(**sz.data)
                persona = Persona(user=user)
                persona.stage = 1  # stage=1 is for new users
                persona.save()
                return Response(sz.data, status=status.HTTP_201_CREATED)
        return Response("Please provide username, email, password, first name and last name.",
                        status=status.HTTP_400_BAD_REQUEST)


class Login(APIView, Meta):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Returns user serialized by UserSerializer plus additional fields if it's politician
        What's returned determine frontend behavior
        """
        username, password = request.data["username"], request.data["password"]
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            # Re-calculates moderator cutoff score whenever any user logs in
            update_scores(pers=Persona.objects.all(), comments=Comment.objects.all())
            # Turning off sweep function for now re-assigns new mods
            # sweep(Persona.objects.all())
            sz = UserSerializer(user)
            persona = user.persona
            try:
                # catches exception when no user hasn't applied as politician yet, probably better way to write this
                pol = persona.politician
                approved = pol.approved
                # need to make relevant serializer
                data = sz.data
                data['approved'] = approved
                data['politician_id'] = pol.id
                return Response(data, status=status.HTTP_202_ACCEPTED)
            except AttributeError:
                data = sz.data
                data['is_mod'] = (persona.stage == 2)
                token, _ = Token.objects.get_or_create(user=user)
                data['token'] = token.key
                return Response(data, status=status.HTTP_200_OK)
        # Helpful to differentiate this from 403 for staff-only views
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Users(APIView, Meta):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        # Staff-only method to get list of all registered users.
        if request.user.is_staff:
            users = User.objects.all()
            sz = UsernameSerializer(users, many=True)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if set(request.data.keys()) == {"user_id", "username", "password"}:
            user = User.objects.get(id=int(request.data["user_id"]), username=request.data["username"],
                                    password=request.data["password"])
            sz = ProfileSerializer(user.persona)
            return Response(sz.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)