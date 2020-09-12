from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from rest_framework import status
from .meta import Meta


class Policies(APIView, Meta):
    policy_attrs = {"category", "name", "statement", "description"}

    @staticmethod
    def by_category(request, c_id):
        # Retrieves policies by category, and optionally index within all policies in that category
        policies = Policy.objects.filter(category=c_id)
        index = int(request.data['index'])
        if len(policies) > index:
            policy = policies[index]
            sz = PolicySerializer(policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        sz = PolicySerializer(policies, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    @staticmethod
    def by_id(id, detailed=False):
        # Retrieves by policy's unique id either the home page preview or full description
        policy = Policy.objects.get(id=id)
        if policy:
            sz = PolicyDetailedSerializer(policy) if detailed else PolicySerializer(policy)
            pop = policy.popularity
            data = sz.data
            data['likes'] = pop.likes
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        """
        This staff only view either updates an existing policy or posts a new one. The checkable fields are in
        PolicyDetailedSerializer, and will be saved if every field passes serializer's field validation.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if "policy_id" in set(request.data.keys()):
            policy = Policy.objects.get(id=int(request.data['policy_id']))
            sz = PolicyDetailedSerializer(policy, data=request.data, partial=True)
            if sz.is_valid(raise_exception=True):
                sz.save()
                return Response(sz.data, status=status.HTTP_200_OK)
        else:
            # No partial=True here cause all fields needed, otherwise serializer throws exception
            sz = PolicyDetailedSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                policy = Policy.objects.create(**sz.data)
                Popularity.objects.create(policy=policy)
                return Response(sz.data, status=status.HTTP_200_OK)
        return Response("Please provide policy_id, category, name, statement and description",
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        id = request.data.get('id')
        policy = Policy.objects.get(id=id)
        policy.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if set(request.GET.keys()) == {'category_id'}:
            return Policies.by_category(request, int(request.GET['category_id']))
        elif set(request.GET.keys()) == {'id'}:
            return Policies.by_id(int(request.GET['id']))
        else:
            sz = PolicySerializer(Policy.objects.all(), many=True)
            return Response(sz.data, status=status.HTTP_200_OK)


class PolicyV(APIView, Meta):
    def get(self, request):
        id = int(request.GET['id'])
        return Policies.by_id(id, detailed=True)

    def put(self, request):
        if set(request.data.keys()) == {"id", "username"}:
            policy = Policy.objects.get(id=int(request.data['id']))
            user = User.objects.get(username=request.data['username'])
            if not policy.users.filter(id=user.id).exists():
                pop = policy.popularity
                pop.likes += 1
                pop.save()
                policy.users.add(user)
                sz = PopularitySerializer(pop)
                return Response(sz.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response("User already liked the policy.", status=status.HTTP_208_ALREADY_REPORTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


