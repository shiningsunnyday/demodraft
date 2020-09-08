from rest_framework.response import Response
from rest_framework.views import APIView
from forward_app.serializers import *
from rest_framework import status
from .meta import Meta


class ThreadV(APIView, Meta):
    @staticmethod
    def thread_comments(thread_id):
        """
        :param thread_id: unique thread id
        :return: serializer for list of comments

        A thread object keeps track of its leading comment's id. Every comment has next comment's id with last one
        leading to itself. This function chains a thread beginning with the leading comment until it reaches a comment
        whose next comment id is itself.
        """
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

    @staticmethod
    def process_thread_set(threads):
        """
        :param thread_id: unique thread id
        :return: serializer for list of comments

        A thread object keeps track of its leading comment's id. Every comment has next comment's id with last one
        leading to itself. This function chains a thread beginning with the leading comment until it reaches a comment
        whose next comment id is itself.
        """
        all_threads = []
        for thread in threads:
            comment = Comment.objects.get(id=thread.lead_comment_id)
            sz = LeadingCommentSerializer(comment)
            data = sz.data
            data['thread_id'] = thread.id
            all_threads.append(data)
        return all_threads

    def get(self, request):
        # Effectively switch statement for allowed sets of GET params, otherwise return 400
        if set(request.GET.keys()) == {"thread_id"}:
            # Returns list of all comments in thread, identified by thread_id
            sz = ThreadV.thread_comments(int(request.GET["thread_id"]))
            return Response(sz.data, status=status.HTTP_200_OK)
        elif set(request.GET.keys()) == {"policy_id"}:
            # Returns list of all threads of policy's popularity, each thread includes the leading comment
            # Returns list of leading comment serializers
            policy = Policy.objects.get(id=int(request.GET["policy_id"]))
            threads = policy.popularity.thread_set.all()
            all_threads = ThreadV.process_thread_set(threads)
            return Response(all_threads, status=status.HTTP_200_OK)
        elif set(request.GET.keys()) == {"politician_id"}:
            # Retrieves list of all threads of politician's constituency, each thread includes the leading comment
            # Returns list of leading comment serializers
            pol = Politician.objects.get(id=int(request.GET["politician_id"]))
            threads = pol.constituency.thread_set.all()
            all_threads = ThreadV.process_thread_set(threads)
            return Response(all_threads, status=status.HTTP_200_OK)
        else:
            return Response("Please provide thread_id or policy_id.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # Effectively switch statement for allowed sets of POST body keys, otherwise return 400
        if set(request.data.keys()) == {"policy_id", "username", "content"}:
            # POST thread with associated policy_id
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
            # POST thread with associated politician_id
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
            # return 400 error 
            return Response("Please provide policy_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)


class CommentV(APIView, Meta):
    @staticmethod
    def append_to_thread(thread_id, username, content):
        """
        :param thread_id: unique thread id
        :param username: username
        :param content: content of comment
        :return: list of comment objects

        This traces a thread to the end for O(n) insertion.
        Let's store last id to thread for O(1) linked list insertion.
        """
        thread = Thread.objects.get(id=thread_id)
        user = User.objects.get(username=username)
        comment = Comment.objects.get(id=thread.lead_comment_id)
        next_comment_id = comment.next_comment_id
        comments = []
        while next_comment_id != comment.id:
            comments.append(comment)
            comment = Comment.objects.get(id=comment.next_comment_id)
            next_comment_id = comment.next_comment_id
        new_comment = Comment.objects.create(user=user, thread=thread, content=content)
        comment.next_comment_id = new_comment.id
        comment.save()
        new_comment.next_comment_id = new_comment.id
        new_comment.save()
        comments.append(comment)
        comments.append(new_comment)
        return comments

    @staticmethod
    def delete_comment(prev_comment_id, username):
        """
        :param prev_comment_id: id of previous comment
        :param username: username
        :return: boolean whether comment was successfully deleted with permission

        Moderators can delete comments.
        """
        user = User.objects.get(username=username)
        stage = user.persona.stage
        if stage == 2:
            comment = Comment.objects.get(id=int(prev_comment_id))
            comment_to_del = Comment.objects.get(id=comment.next_comment_id)
            if comment_to_del.id != comment_to_del.next_comment_id:
                # not the last comment
                next_comment = Comment.objects.get(id=comment_to_del.next_comment_id)
                comment.next_comment_id = next_comment.id
                comment_to_del.delete()
                comment.save()
            else:
                # last comment
                comment_to_del.delete()
                comment.next_comment_id = comment.id
                comment.save()
            return True
        return False

    def post(self, request):
        if set(request.data.keys()) == {"thread_id", "username", "content"}:
            # POST comment to assoicated thread_id
            sz = NextCommentSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                comments = CommentV.append_to_thread(**request.data)
                sz = CommentSerializer(comments, many=True)
                return Response(sz.data, status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif set(request.data.keys()) == {"username", "prev_comment_id"}:
            ret_204 = Response("You've deleted the comment.", status=status.HTTP_204_NO_CONTENT)
            ret_400 = Response("You are not authorized to delete comments.", status=status.HTTP_400_BAD_REQUEST)
            return ret_204 if CommentV.delete_comment(**request.data) else ret_400
        else:
            # return 400 error
            return Response("Please provide thread_id, username, and content.", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def like_comment(comment_id, username=""):
        """
        :param comment_id: unique id of comment
        :param username: username of user
        :return: serialized comment

        The likes goes through only if default empty string username given or username is not same as comment's OP.
        """
        comment = Comment.objects.get(id=comment_id)
        if not username or comment.user.username != username:
            comment.likes += 1
            comment.save()
        return CommentSerializer(comment)

    def patch(self, request):
        sz = None
        if set(request.data.keys()) in [{"comment_id"}, {"username", "comment_id"}]:
            # Python kwargs takes care of both cases
            sz = CommentV.like_comment(**request.data)
        else:
            return Response("Please provide comment_id.", status=status.HTTP_400_BAD_REQUEST)
        return Response(sz.data, status=status.HTTP_200_OK)

    def put(self, request):
        if set(request.data.keys()) != {"comment_id", "content"}:
            return Response("Please provide comment_id, and updated content.", status=status.HTTP_400_BAD_REQUEST)
        sz = UpdatedCommentSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            # Update comment associated with valid comment_id
            comment = Comment.objects.get(id=request.data["comment_id"])
            comment.content = request.data["content"]
            comment.save()
            sz = CommentSerializer(comment)
            return Response(sz.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
