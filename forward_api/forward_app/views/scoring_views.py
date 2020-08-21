from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *
from forward_app.utils.score_system import *


class Score(APIView, Meta):
    def get(self, request):
        update_scores(pers=Persona.objects.all(), comments=Comment.objects.all())
        sweep(Persona.objects.all())
        sz = PersonaSerializer(Persona.objects.all(), many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

