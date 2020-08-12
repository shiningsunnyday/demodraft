from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress, merge
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *


class StanceV(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) != {"policy_id", "politician_id", "content"}:
            return Response("Please provide policy_id, politician_id, and content.", status=status.HTTP_400_BAD_REQUEST)
        policy = Policy.objects.get(id=int(request.data['policy_id']))
        pol = Politician.objects.get(id=int(request.data['politician_id']))
        stance = Stance.objects.create(politician=pol, policy=policy, message=request.data['content'])
        sz = StanceSerializer(stance)
        return Response(sz.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        if set(request.GET.keys()) == {"politician_id"}:
            pol = Politician.objects.get(id=int(request.GET['politician_id']))
            stances = pol.stance_set.all()
            sz = StanceSerializer(stances, many=True)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)