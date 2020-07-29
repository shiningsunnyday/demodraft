from django.test import TestCase
from django.test import Client
from forward_app.core_models import Policy
from forward_app.core_models import Comment
from forward_app.core_models import Popularity

"""
Tests for all functionality with Policy object
"""
class PolicyTest(TestCase):

    def setUp(self):
        Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all', description='Medical services to all citizens')

    def testCategory(self):
        policy = Policy.objects.get(category=1)
        self.assertEqual(policy.category, 1)

    # def testName(self):
    #     policy = Policy.objects.get(name='Universal Health Care')
    #     self.assertEqual(policy.name, 'Universal Health Care')

    # def testDescription(self):
    #     policy = Policy.objects.get(description='Medical services to all citizens')
    #     self.assertEqual(policy.description, 'Medical services to all citizens')

    # def testStatement(self):
    #     policy = Policy.objects.get(statement='Healthcare for all')
    #     self.assertEqual(policy.statement, 'Healthcare for all')

    # def testPopularity(self):
    #     policy1 = Policy.objects.get(category='Healthcare')
    #     popularity = Popularity.objects.create(policy=policy1, likes=200, endorsements=50, visits=1000)
    #     self.assertEquals(popularity.likes,200)
    #     self.assertEquals(popularity.endorsements, 50)
    #     self.assertEquals(popularity.visits, 1000)

