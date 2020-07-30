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
        policy = Policy.objects.get(category=1)
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

    def testPopularity(self):
        policy1 = Policy.objects.get(category=1)
        popularity = Popularity.objects.create(policy=policy1, likes=200, visits=1000)
        self.assertEquals(popularity.likes,200)
        self.assertEquals(popularity.visits, 1000)
        self.assertEqual(popularity.policy, policy1)

"""
Tests for all functionality with Comment object
"""

class CommentTest(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')

    def testComments(self):
        user = User.objects.create_user(username='brian')
        policy = Policy.objects.get(category=1)
        popularity = Popularity.objects.create(policy=policy, likes=20, visits=1000)
        comment = Comment.objects.create(popularity = popularity, username=user, content='good policy', likes=5)
        self.assertEqual(comment.popularity, popularity)
        self.assertEqual(comment.username,user)
        self.assertEqual(comment.content,'good policy')
        self.assertEquals(comment.likes,5)

    def testCommentChain(self):
        user = User.objects.create_user(username='brian')
        policy = Policy.objects.get(category=1)
        popularity = Popularity.objects.create(policy=policy, likes=20, visits=1000)
        comment3 = Comment.objects.create(popularity=popularity, username=user, content='good policy', likes=5)
        comment2 = Comment.objects.create(popularity=popularity, next_comment_id=comment3.id, username=user, content='I agree', likes=2)
        comment1 = Comment.objects.create(popularity=popularity, next_comment_id=comment2.id, username=user, content='Yang Gang!', likes=7)
        self.assertEqual(comment3.id,1)
        self.assertEqual(comment3.next_comment_id, 0)
        self.assertEqual(comment2.next_comment_id, comment3.id)
        self.assertEqual(comment1.next_comment_id, comment2.id)

"""
Tests for all functionality with Thread object
"""
class TestThread(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')

    def testThread(self):
        user = User.objects.create_user(username='brian')
        policy = Policy.objects.get(category=1)
        popularity = Popularity.objects.create(policy=policy, likes=20, visits=1000)
        comment2 = Comment.objects.create(popularity=popularity, username=user, content='I like this', likes=2)
        comment1 = Comment.objects.create(popularity=popularity, next_comment_id=comment2.id, username=user, content='I do not like this', likes=7)
        thread = Thread.objects.create(popularity = popularity, lead_comment_id=comment1.id)
        self.assertEqual(thread.lead_comment_id, 2)
        self.assertEqual(thread.popularity, popularity)



        



