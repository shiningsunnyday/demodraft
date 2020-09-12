from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress, merge
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *


class PlanV(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) == {"policy_id", "politician_id", "steps", "scope"}:
            policy_id, politician_id = int(request.data["policy_id"]), int(request.data["politician_id"])
            politician = Politician.objects.get(id=politician_id)
            policy = Policy.objects.get(id=policy_id)
            if not Stance.objects.filter(policy_id=policy_id, politician_id=politician_id).exists():
                return Response("Please create stance first.", status=status.HTTP_400_BAD_REQUEST)
            stance = Stance.objects.get(politician=politician, policy=policy)
            if Plan.objects.filter(stance=stance).exists():
                return Response("Plan already exists.", status=status.HTTP_400_BAD_REQUEST)
            assert isinstance(request.data['steps'], list) and len(request.data['steps']) > 0
            step = Step.objects.create(description=request.data['steps'][0])
            lead_step_id = step.id
            plan = Plan(stance=stance)
            plan_sz = PlanSerializer(plan, data={"lead_step_id": lead_step_id, "scope": request.data["scope"]},
                                     partial=True)
            if plan_sz.is_valid(raise_exception=True):
                plan_sz.save()
            plan = Plan.objects.get(stance=stance)
            for step_descr in request.data['steps'][1:]:
                next_step = Step.objects.create(description=step_descr, plan=plan)
                next_step.next_step_id = next_step.id
                next_step.save()
                step.next_step_id = next_step.id
                step.save()
                step = next_step
            plan_sz = PlanSerializer(plan)
            return Response(plan_sz.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if set(request.GET.keys()) == {"policy_id", "politician_id"}:
            policy_id, politician_id = int(request.GET["policy_id"]), int(request.GET["politician_id"])
            politician = Politician.objects.get(id=politician_id)
            policy = Policy.objects.get(id=policy_id)
            stance = Stance.objects.get(politician=politician, policy=policy)
            if Plan.objects.filter(stance=stance).exists():
                plan = Plan.objects.get(stance=stance)
                plan_sz = PlanSerializer(plan)
                return Response(plan_sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)