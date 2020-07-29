from django.contrib.auth.models import User
from forward_app.core_models import Politician, Policy
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class PoliticianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Politician
        fields = ['name']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['created', 'category', 'name', 'statement']


class PolicyDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['created', 'category', 'name', 'statement', 'description']