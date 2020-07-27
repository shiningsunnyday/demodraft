from django.test import TestCase
from django.test import Client
from forward_app.core_models import Politician

"""
Tests for all functionality with Politician object
"""
class PoliticianTest(TestCase):

    def setUp(self):
        Politician.objects.create(name="George Washington")

    def testName(self):
        politician = Politician.objects.get(name="George Washington")
        self.assertEqual(politician.name, "George Washington")