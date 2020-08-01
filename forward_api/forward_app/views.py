from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status


class Meta(object):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]


class Signup(APIView, Meta):
    def post(self, request):
        username, email, password = request.data["username"], request.data["email"], request.data["password"]
        sz = UserSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Login(APIView, Meta):
    def post(self, request):
        username, password = request.data["username"], request.data["password"]
        user = authenticate(username=username, password=password)
        if user:
            sz = UserSerializer(user)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Users(APIView, Meta):
    def get(self, request):
        users = User.objects.all()
        sz = UserSerializer(users, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)


class Policies(APIView, Meta):
    @staticmethod
    def by_category(request, c_id):
        policies = Policy.objects.filter(category=c_id)
        index = request.data.get('index')
        if index != None and isinstance(index, int):
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
        policy = Policy.objects.get(id=id)
        if policy:
            sz = PolicyDetailedSerializer(policy) if detailed else PolicySerializer(policy)
            pop = policy.popularity
            data = sz.data
            data['likes'] = pop.likes
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if set(request.data.keys()) != {"category", "name", "statement", "description"}:
            return Response("Please provide category, name, statement and description.",
                            status=status.HTTP_400_BAD_REQUEST)

        sz = PolicyDetailedSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            policy = Policy.objects.create(**sz.data)
            pop = Popularity.objects.create(policy=policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.data.get('id')
        policy = Policy.objects.get(id=id)
        policy.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        c_id = request.data.get('category_id')
        if c_id != None and isinstance(c_id, int):
            return Policies.by_category(request, c_id)
        id = request.data.get('id')
        if id != None and isinstance(id, int):
            return Policies.by_id(id)
        sz = PolicySerializer(Policy.objects.all(), many=True)

        return Response(sz.data, status=status.HTTP_200_OK)


class PolicyV(APIView, Meta):
    def get(self, request):
        id = int(request.GET['id'])
        return Policies.by_id(id, detailed=True)

    def put(self, request):
        id = request.data.get('id')
        policy = Policy.objects.get(id=id)
        pop = policy.popularity
        pop.likes += 1
        pop.save()
        sz = PopularitySerializer(pop)
        return Response(sz.data, status=status.HTTP_202_ACCEPTED)


class ThreadV(APIView, Meta):
    @staticmethod
    def thread_comments(thread_id):
        thread = Thread.objects.get(id=thread_id)
        comment = Comment.objects.get(id=thread.lead_comment_id)
        next_comment_id = comment.next_comment_id
        comments = [comment]
        while next_comment_id != comment.id:
            comment = Comment.objects.get(id=comment.next_comment_id)
            next_comment_id = comment.next_comment_id
            comments.append(comment)
        sz = CommentSerializer(comments, many=True)
        return sz

    def get(self, request):
        if set(request.GET.keys()) == {"thread_id"}:
            sz = ThreadV.thread_comments(int(request.GET["thread_id"]))
            return Response(sz.data, status=status.HTTP_200_OK)
        elif set(request.GET.keys()) == {"policy_id"}:
            policy = Policy.objects.get(id=int(request.GET["policy_id"]))
            threads = policy.popularity.thread_set.all()
            all_threads = []
            for thread in threads:
                sz = ThreadV.thread_comments(thread.id)
                all_threads.append(sz.data)
            return Response(all_threads, status=status.HTTP_200_OK)
        else:
            return Response("Please provide thread_id or policy_id.", status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        if set(request.data.keys()) != {"policy_id", "username", "content"}:
            return Response("Please provide policy_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)
        sz = FirstCommentSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            policy = Policy.objects.get(id=request.data["policy_id"])
            popularity = policy.popularity
            thread = Thread.objects.create(popularity=popularity)
            user = User.objects.get(username=sz.data["username"])
            comment = Comment.objects.create(user=user, thread=thread, content=sz.data["content"])
            thread.lead_comment_id = comment.id
            comment.next_comment_id = comment.id
            thread.save()
            comment.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentV(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) != {"thread_id", "username", "content"}:
            return Response("Please provide thread_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)
        sz = NextCommentSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            thread = Thread.objects.get(id=request.data["thread_id"])
            user = User.objects.get(username=request.data["username"])

            comment = Comment.objects.get(id=thread.lead_comment_id)
            next_comment_id = comment.next_comment_id
            comments = []
            while next_comment_id != comment.id:
                comments.append(comment)
                comment = Comment.objects.get(id=comment.next_comment_id)
                next_comment_id = comment.next_comment_id
            new_comment = Comment.objects.create(user=user, thread=thread, content=request.data["content"])
            comment.next_comment_id = new_comment.id
            comment.save()
            new_comment.next_comment_id = new_comment.id
            new_comment.save()
            comments.append(comment)
            comments.append(new_comment)
            sz = CommentSerializer(comments, many=True)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if set(request.data.keys()) != {"comment_id"}:
            return Response("Please provide comment_id.", status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.get(id=request.data["comment_id"])
        comment.likes += 1
        comment.save()
        sz = CommentSerializer(comment)
        return Response(sz.data, status=status.HTTP_200_OK)

    def put(self, request):
        if set(request.data.keys()) != {"comment_id", "content"}:
            return Response("Please provide comment_id, and updated content.", status=status.HTTP_400_BAD_REQUEST)
        sz = UpdatedCommentSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            comment = Comment.objects.get(id=request.data["comment_id"])
            comment.content = request.data["content"]
            comment.save()
            sz = CommentSerializer(comment)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

