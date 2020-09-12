from django.contrib.auth.models import User
from forward_app.core_models import *
from rest_framework import serializers
from forward_app.utils.email_csv import search


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, email):
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise serializers.ValidationError("Email already exists.")
        return email

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['user', 'stage', 'score']


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['num_followers']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['line1', 'city', 'state', 'zipcode']


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
    state = serializers.SerializerMethodField("get_loc")

    def get_username(self, pol):
        return pol.persona.user.username

    def get_loc(self, pol):
        return pol.persona.state
    
    class Meta:
        model = Politician
        fields = ['id', 'name', 'state', 'username', 'first', 'last', 'approved']


class PlanSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField("get_address")
    steps = serializers.SerializerMethodField("get_steps")

    def get_steps(self, plan):
        step = Step.objects.get(id=plan.lead_step_id)
        next_step_id = step.next_step_id
        steps = []
        while next_step_id != step.id:
            steps.append(step.description)
            step = Step.objects.get(id=step.next_step_id)
            next_step_id = step.next_step_id
        return steps

    def get_address(self, plan):
        i = Plan.SCOPES.index(plan.scope)
        pers = plan.politician.persona
        return ", ".join([pers.city, pers.state, "US"][i:])

    class Meta:
        model = Plan
        fields = ['id', 'lead_step_id', 'politician_id', 'address', 'scope', 'steps']

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
    likes = serializers.SerializerMethodField("get_likes")

    def get_likes(self, policy):
        pop = policy.popularity
        return pop.likes

    class Meta:
        model = Policy
        fields = ['id', 'created', 'category', 'name', 'statement', 'likes']


class PolicyDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'created', 'category', 'name', 'statement', 'description']


class PopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularity
        fields = ['likes']


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField("get_email")

    def get_email(self, pers):
        return pers.user.email

    class Meta:
        model = Persona
        fields = ['stage', 'email', 'score']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")
    first_name = serializers.SerializerMethodField("get_first")
    last_name = serializers.SerializerMethodField("get_last")

    def get_username(self, comment):
        return comment.user.username

    def get_first(self, comment):
        return comment.user.first_name

    def get_last(self, comment):
        return comment.user.last_name

    class Meta:
        model = Comment
        fields = ['id', 'time', 'username', 'next_comment_id', 'first_name', 'last_name', 'content', 'likes']


class LeadingCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")
    first_name = serializers.SerializerMethodField("get_first")
    last_name = serializers.SerializerMethodField("get_last")

    def get_username(self, comment):
        return comment.user.username

    def get_first(self, comment):
        return comment.user.first_name

    def get_last(self, comment):
        return comment.user.last_name

    class Meta:
        model = Comment
        fields = ['id', 'time', 'username', 'first_name', 'last_name', 'content', 'likes']


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


class FirstPolCommentSerializer(serializers.ModelSerializer):
    politician_id = serializers.IntegerField(min_value=1)
    username = serializers.CharField(max_length=150)
    content = serializers.CharField(max_length=1000)

    def validate_politician_id(self, id):
        exists = Politician.objects.filter(id=id).exists()
        if not exists:
            raise serializers.ValidationError("Politician doesn't exist.")
        return id

    def validate_username(self, username):
        exists = User.objects.filter(username=username).exists()
        if not exists:
            raise serializers.ValidationError("Username doesn't exist.")
        return username

    class Meta:
        model = Thread
        fields = ['id', 'politician_id', 'username', 'content']


class NextCommentSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(min_value=1)
    username = serializers.SerializerMethodField("get_username")
    first_name = serializers.SerializerMethodField("get_first")
    last_name = serializers.SerializerMethodField("get_last")

    def get_username(self, comment):
        return comment.user.username

    def get_first(self, comment):
        return comment.user.first_name

    def get_last(self, comment):
        return comment.user.last_name

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
        fields = ['id', 'thread_id', 'username', 'first_name', 'last_name', 'content']


class StanceSerializer(serializers.ModelSerializer):
    policy_id = serializers.SerializerMethodField("get_policy_id")
    policy_name = serializers.SerializerMethodField("get_policy_name")

    def get_policy_id(self, stance):
        return stance.policy.id

    def get_policy_name(self, stance):
        return stance.policy.name

    class Meta:
        model = Stance
        fields = ['id', 'policy_id', 'policy_name', 'message', 'date']


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