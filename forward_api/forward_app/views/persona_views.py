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
                return Response("A non-existent username or politician id was used", status=status.HTTP_400_BAD_REQUEST)

            isFollowing = request.data["isFollowing"]
            pers = pol.persona
            us = pers.user
            if not pers.users.filter(id=user.id).exists():
                if isFollowing is True:
                    pers.users.add(user)
                    pers.num_followers += 1
                else:
                    return Response("Not following " + us.first_name+" "+ us.last_name, status=status.HTTP_400_BAD_REQUEST)
            else:
                if isFollowing is False:
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
        

        followings = Following.objects.raw('SELECT * FROM forward_app_persona_users')
        users = []
        #get followers for politician
        if set(request.data.keys()) == {"politician_id"}:

            try:
                user = Politician.objects.get(id=request.data["politician_id"]).persona.user
            except:
                return Response("Politician does not exist", status=status.HTTP_400_BAD_REQUEST)

            for f in followings:
                if f.user_id == user.id:
                    users.append(Persona.objects.get(id=f.persona_id).user)
                    print(f.user_id)
        else:

            per = None
            #get following for specific user
            if set(request.data.keys()) == {"username"}:
                try:
                    per = User.objects.get(username=request.data["username"]).persona
                except:
                    return Response("User with username " + request.data["username"] + " does not exist", status=status.HTTP_400_BAD_REQUEST)

            #get following for logged in user
            elif request.user.is_authenticated():
                per = request.user.persona
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            for f in followings:
                if f.persona_id == per.id:
                    users.append(User.objects.get(id=f.user_id))

        sz = UsernameSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

class polFollowings(APIView, Meta):

    def get(self, request):

        if set(request.data.keys()) == {"politician_id"}:

            try:
                user = Politician.objects.get(id=request.data["politician_id"]).persona.user
            except:
                return Response("Politician does not exist", status=status.HTTP_400_BAD_REQUEST)

            politicians = Politician.objects.raw('SELECT id FROM forward_app_politician WHERE approved IS 1 AND id IS NOT '+str(request.data["politician_id"]))
            pol_user_ids = []
            users = []

            for p in politicians:
                pol_user_ids.append(p.persona.id)
            print(pol_user_ids)

            followings = Following.objects.raw('SELECT * FROM forward_app_persona_users')

            for f in followings:
                if f.user_id == user.id:
                    if f.persona_id in pol_user_ids:
                        users.append(Persona.objects.get(id=f.persona_id).user)

        sz = UsernameSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)