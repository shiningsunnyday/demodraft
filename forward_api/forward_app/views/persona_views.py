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
            isFollowing = request.data["isFollowing"]
            pol = Politician.objects.get(id=int(request.data["politician_id"]))
            user = User.objects.get(username=request.data["username"])
            pers = pol.persona
            us = pers.user
            if not pers.users.filter(id=user.id).exists():
                if request.data["isFollowing"] is true:
                    pers.users.add(user)
                    pers.num_followers += 1
                else:
                    return Response("Not following " + us.first_name+" "+ us.last_name, status=status.HTTP_400_BAD_REQUEST)
            else:
                if request.data["isFollowing"] is false:
                    pers.users.remove(user)
                    pers.num_followers -= 1
                else:
                    return Response("Already following " + us.first_name+" "+ us.last_name, status=status.HTTP_400_BAD_REQUEST)
            pers.save()
            sz = FollowersSerializer(pers)
            return Response(sz.data, status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class Followings(APIView, Meta):

    def get(self, request):
        
        per = None
        users = []

        if set(request.data.keys()) == {"username"}:
            per = User.objects.get(id=data["username"]).persona

        elif set(request.data.keys()) == {"politician_id"}:
            per = Politician.objects.get(id=request.data["politician_id"]).persona
            for p in per.users:
                users.append[Persona.objects.get(id=p.persona_id).user]

        elif request.user.is_authenticated():
            per = request.user.persona

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        sz = UsernameSerializer(users, many=True)
        return Response(sz, status=status.HTTP_200_OK)