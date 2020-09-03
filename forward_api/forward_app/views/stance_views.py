from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress, merge
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *


class StanceV(APIView, Meta):
    def post(self, request):
        """
        This creates a Stance object using the through= keyword argument.
        https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ManyToManyField.through_fields
        """
        if set(request.data.keys()) != {"policy_id", "politician_id", "content"}:
            return Response("Please provide policy_id, politician_id, and content.", status=status.HTTP_400_BAD_REQUEST)
        policy_id, politician_id = int(request.data['policy_id']), int(request.data['politician_id'])
        if Stance.objects.filter(policy_id=policy_id, politician_id=politician_id).exists():
            return Response("Stance already exists for politician and policy.", status=status.HTTP_400_BAD_REQUEST)
        policy = Policy.objects.get(id=policy_id)
        pol = Politician.objects.get(id=politician_id)
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

    def put(self, request):
        if set(request.data.keys()) != {"stance_id", "message"}:
            return Response("Please provide stance_id and message.", status=status.HTTP_400_BAD_REQUEST)
        stance = Stance.objects.get(id=int(request.data['stance_id']))
        sz = StanceSerializer(stance, data=request.data, partial=True)  # pass partial=True if not updating all fields
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
