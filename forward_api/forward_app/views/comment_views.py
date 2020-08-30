from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from rest_framework import status
from .meta import Meta


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
        elif set(request.GET.keys()) == {"politician_id"}:
            pol = Politician.objects.get(id=int(request.GET["politician_id"]))
            threads = pol.constituency.thread_set.all()
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
        elif set(request.data.keys()) == {"politician_id", "username", "content"}:
            sz = FirstPolCommentSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                pol = Politician.objects.get(id=request.data["politician_id"])
                constituency = pol.constituency
                thread = Thread.objects.create(constituency=constituency)
                user = User.objects.get(username=sz.data["username"])
                comment = Comment.objects.create(user=user, thread=thread, content=sz.data["content"])
                thread.lead_comment_id = comment.id
                comment.next_comment_id = comment.id
                thread.save()
                comment.save()
                return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Please provide policy_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)


class CommentV(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) == {"thread_id", "username", "content"}:
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
        elif set(request.data.keys()) == {"username", "prev_comment_id"}:
            user = User.objects.get(username=request.data["username"])
            stage = user.persona.stage
            if stage == 2:
                comment = Comment.objects.get(id=int(request.data["prev_comment_id"]))
                comment_to_del = Comment.objects.get(id=comment.next_comment_id)
                if comment_to_del.id != comment_to_del.next_comment_id:
                    next_comment = Comment.objects.get(id=comment_to_del.next_comment_id)
                    comment.next_comment_id = next_comment.id
                    comment_to_del.delete()
                    comment.save()
                else:
                    comment_to_del.delete()
                    comment.next_comment_id = comment.id
                    comment.save()
                return Response("You've deleted the comment.", status=status.HTTP_204_NO_CONTENT)
            return Response("You are not authorized to delete comments.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please provide thread_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)

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
