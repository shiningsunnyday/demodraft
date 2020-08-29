from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from rest_framework import status
from .meta import Meta


class Policies(APIView, Meta):
    policy_attrs = {"category", "name", "statement", "description"}
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
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if "policy_id" in set(request.data.keys()):
            policy = Policy.objects.get(id=int(request.data['policy_id']))
            for k in request.data.keys():
                if k not in Policies.policy_attrs and k != 'policy_id':
                    return Response("Please provide only category, name, statement and description.",
                                    status=status.HTTP_400_BAD_REQUEST)
                setattr(policy, k, request.data[k])
            policy.save()
            sz = PolicyDetailedSerializer(policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        if set(request.data.keys()) != Policies.policy_attrs:
            return Response("Please provide category, name, statement and description.",
                            status=status.HTTP_400_BAD_REQUEST)

        sz = PolicyDetailedSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            policy = Policy.objects.create(**sz.data)
            pop = Popularity.objects.create(policy=policy)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
                comment = Comment.objects.get(id=thread.lead_comment_id)
                sz = LeadingCommentSerializer(comment)
                data = sz.data
                data['thread_id'] = thread.id
                all_threads.append(data)
            return Response(all_threads, status=status.HTTP_200_OK)
        else:
            return Response("Please provide thread_id or policy_id.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if set(request.data.keys()) == {"policy_id", "username", "content"}:
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
        elif set(request.data.keys()) == {"thread_id", "username"}:
            user = User.objects.get(username=request.data["username"])
            stage = user.persona.stage
            if stage == 2:
                thread = Thread.objects.get(id=int(request.data["thread_id"]))
                # delete comments associated with thread
                cur_comment_id = thread.lead_comment_id
                comment = Comment.objects.get(id=cur_comment_id)
                while cur_comment_id != comment.next_comment_id:
                    cur_comment_id = comment.next_comment_id
                    comment.delete()
                    comment = Comment.objects.get(id=cur_comment_id)
                comment.delete()
                thread.delete()
                return Response("You've deleted the thread.", status=status.HTTP_204_NO_CONTENT)
            return Response("You are not authorized to delete threads.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please provide policy_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)
