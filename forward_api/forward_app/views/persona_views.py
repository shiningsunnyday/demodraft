from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *
from forward_app.utils.score_system import *


class PersonaV(APIView, Meta):
    def get(self, request):
        update_scores(pers=Persona.objects.all(), comments=Comment.objects.all())
        sweep(Persona.objects.all())
        sz = PersonaSerializer(Persona.objects.all(), many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    def put(self, request):
        # including this under PersonaV because it's the pers's fields being altered
        if set(request.data.keys()) == {"politician_id", "username", "isFollowing"}:
            try:
                pol = Politician.objects.get(id=int(request.data["politician_id"]))
                user = User.objects.get(username=request.data["username"])
            except:
                return Response("A non-existent username or politician id was used", status=status.HTTP_404_NOT_FOUND)

            isFollowing = request.data["isFollowing"]
            pers = pol.persona
            us = pers.user
            if not pers.users.filter(id=user.id).exists():
                if isFollowing:
                    if pers.user.id == user.id:
                        return Response("Can not follow yourself", status=status.HTTP_403_FORBIDDEN)

                    pers.users.add(user)
                    pers.num_followers += 1
                else:
                    return Response("Not following " + us.first_name+" "+ us.last_name, status=status.HTTP_403_FORBIDDEN)
            else:
                if not isFollowing:
                    pers.users.remove(user)
                    pers.num_followers -= 1
                else:
                    return Response("Already following " + us.first_name+" "+ us.last_name, status=status.HTTP_403_FORBIDDEN)
            pers.save()
            sz = FollowersSerializer(pers)
            return Response(sz.data, status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class Followings(APIView, Meta):

    def get(self, request):

        users = []

        #get followers for politician
        if set(request.data.keys()) == {"politician_id"}:

            try:
                per = Politician.objects.get(id=request.data["politician_id"]).persona
            except:
                return Response("Politician does not exist", status=status.HTTP_404_NOT_FOUND)

            users = per.users.all()

        else:
            #get followings for specific user
            user = None
            if set(request.data.keys()) == {"username"}:
                try:
                    user = User.objects.get(username=request.data["username"])
                except:
                    return Response("User with username " + request.data["username"] + " does not exist", status=status.HTTP_404_NOT_FOUND)

            #get following for logged in user
            elif request.user.is_authenticated():
                user = request.user
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            followings = Following.objects.raw('SELECT * FROM forward_app_persona_users')

            for f in followings:
                if f.user_id == user.id:
                    users.append(Persona.objects.get(id=f.persona_id).user)

        sz = UsernameSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

class polFollowings(APIView, Meta):

    #get all politicians following a specific politician
    def get(self, request):

        if set(request.data.keys()) == {"politician_id"}:

            try:
                per = Politician.objects.get(id=request.data["politician_id"]).persona
            except:
                return Response("Politician does not exist", status=status.HTTP_404_NOT_FOUND)

            politicians = Politician.objects.filter(approved=1).exclude(id=request.data["politician_id"])
            pol_user_ids = []
            users = []

            for p in politicians:
                pol_user_ids.append(p.persona.user.id)

            for u in per.users.all():
                if u.id in pol_user_ids:
                    users.append(u)

        sz = UsernameSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)