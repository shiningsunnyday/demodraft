from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from forward_app.core_models import Policy
from forward_app.core_models import Comment
from forward_app.core_models import Popularity
from forward_app.core_models import Thread

"""
Tests for all functionality with Policy object
"""
class PolicyTest(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')

    def testCategory(self):
        policy = Policy.objects.get(name='Universal Health Care')
        self.assertEqual(policy.category, 1)

    def testStatement(self):
        policy = Policy.objects.get(name='Universal Health Care')
        self.assertEqual(policy.statement, 'Healthcare for all')

    def testDescription(self):
        policy = Policy.objects.get(description='Medical services to all citizens')
        self.assertEqual(policy.description, 'Medical services to all citizens')

"""
Tests for all functionality with Popularity object
"""

class PopularityTest(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')
        User.objects.create(username="michael")

    def testPopularity(self):
        policy = Policy.objects.get(name='Universal Health Care')
        popularity = Popularity.objects.create(policy=policy, likes=200)
        self.assertEquals(popularity.likes, 200)
        self.assertEqual(popularity.policy, policy)

    def testLike(self):
        # makes sure user who liked can't like again
        pol = Policy.objects.get(id=1)
        user = User.objects.get(id=1)
        pol.users.add(user)
        self.assertEqual(True, pol.users.filter(id=user.id).exists())

"""
Tests for all functionality with Comment object
"""

class CommentTest(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')

    def testComment(self):
        user = User.objects.create_user(username='brian')
        policy = Policy.objects.get(name='Universal Health Care')
        popularity = Popularity.objects.create(policy=policy, likes=20)
        thread = Thread.objects.create(popularity=popularity)

        comment = Comment.objects.create(user=user, thread=thread, content='good policy', likes=5)
        thread.lead_comment_id = comment.id
        comment.next_comment_id = comment.id

        self.assertEqual(thread.popularity, popularity)
        self.assertEqual(comment.user, user)
        self.assertEqual(comment.content, 'good policy')
        self.assertEqual(comment.likes, 5)


    def testThread(self):
        user = User.objects.create_user(username='brian')
        policy = Policy.objects.get(name='Universal Health Care')
        popularity = Popularity.objects.create(policy=policy, likes=20)
        thread = Thread.objects.create(popularity=popularity)
        comment = Comment.objects.create(user=user, thread=thread, content='good policy', likes=5)
        thread.lead_comment_id = comment.id
        comment.next_comment_id = comment.id

        comment2 = Comment.objects.create(user=user, thread=thread, content='I agree', likes=2)
        comment2.next_commend_id = comment2.id
        comment.next_comment_id = comment2.id


        self.assertEqual(Comment.objects.get(id=thread.lead_comment_id), comment)
        self.assertEqual(comment.next_comment_id, comment2.id)






        



