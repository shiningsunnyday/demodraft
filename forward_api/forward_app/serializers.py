from django.contrib.auth.models import User
from forward_app.core_models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, email):
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise serializers.ValidationError("Email already exists.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class PoliticianSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    def get_username(self, pol):
        return pol.persona.user.username
    
    class Meta:
        model = Politician
        fields = ['id', 'name', 'username', 'first', 'last', 'approved']


class CampaignSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("office_name")
    first = serializers.SerializerMethodField("get_first")
    last = serializers.SerializerMethodField("get_last")

    def office_name(self, camp):
        return camp.politician.name

    def get_first(self, camp):
        return camp.politician.first

    def get_last(self, camp):
        return camp.politician.last

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'first', 'last', 'actblue', 'fundraised']


class MyCampaignSerializer(CampaignSerializer):
    approved = serializers.SerializerMethodField("is_approved")

    def is_approved(self, camp):
        pol = camp.politician
        return pol.approved

    class Meta:
        model = Campaign
        fields = ['id', 'approved', 'name', 'first', 'last', 'actblue', 'fundraised', 'fundraise_goal']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'created', 'category', 'name', 'statement']


class PolicyDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'created', 'category', 'name', 'statement', 'description']


class PopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularity
        fields = ['likes']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    def get_username(self, comment):
        return comment.user.username

    class Meta:
        model = Comment
        fields = ['id', 'time', 'username', 'next_comment_id', 'content', 'likes']


class LeadingCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    def get_username(self, comment):
        return comment.user.username

    class Meta:
        model = Comment
        fields = ['id', 'time', 'username', 'content', 'likes']


class UpdatedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id']


class FirstCommentSerializer(serializers.ModelSerializer):
    policy_id = serializers.IntegerField(min_value=1)
    username = serializers.CharField(max_length=150)
    content = serializers.CharField(max_length=1000)

    def validate_policy_id(self, id):
        exists = Policy.objects.filter(id=id).exists()
        if not exists:
            raise serializers.ValidationError("Policy doesn't exist.")
        return id

    def validate_username(self, username):
        exists = User.objects.filter(username=username).exists()
        if not exists:
            raise serializers.ValidationError("Username doesn't exist.")
        return username

    class Meta:
        model = Thread
        fields = ['id', 'policy_id', 'username', 'content']


class NextCommentSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(min_value=1)
    username = serializers.CharField(max_length=150)

    def validate_thread_id(self, id):
        exists = Thread.objects.filter(id=id).exists()
        if not exists:
            raise serializers.ValidationError("Thread doesn't exist.")
        return id

    def validate_username(self, username):
        exists = User.objects.filter(username=username).exists()
        if not exists:
            raise serializers.ValidationError("Username doesn't exist.")
        return username

    class Meta:
        model = Comment
        fields = ['id', 'thread_id', 'username', 'content']


# class AllThreads(serializers.ModelSerializer):
#     def to_representation(self, popularity):
#         threads = popularity.thread_set
#         repr = super().to_representation(threads)
#         repr["comments"] = []
#         for thread in threads:
#             comment_id = thread.lead_comment_id
#             comment = Comment.objects.get(id=comment_id)
#             comment_sz = CommentSerializer(comment)
#             repr["comments"].append(comment_sz.data)
#         return repr
#     class Meta:
#         model = Popularity