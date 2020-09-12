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
        if set(request.data.keys()) == {"politician_id", "username"}:
            pol = Politician.objects.get(id=int(request.data["politician_id"]))
            user = User.objects.get(username=request.data["username"])
            pers = pol.persona
            if not pers.users.filter(id=user.id).exists():
                pers.users.add(user)
                pers.num_followers += 1
                pers.save()
            sz = FollowersSerializer(pers)
            return Response(sz.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)