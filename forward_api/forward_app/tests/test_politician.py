from django.test import TestCase
from django.test import Client
from forward_app.core_models import Politician
from forward_app.core_models import Persona
from django.contrib.auth.models import User
from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress


"""
Tests for all functionality with Politician object
"""
class PoliticianTest(TestCase):

    def testPolitician(self):
        user = User.objects.create_user(username="brian")
        persona = Persona.objects.create(user=user, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        politician = Politician.objects.create(persona=persona, office_id=1, office_name="brian's office", fundraised=100, fundraise_goal=10000)
        self.assertEqual(politician.office_id, 1)
        self.assertEqual(politician.office_name, "brian's office")
        self.assertEqual(politician.fundraised, 100)
        self.assertEqual(politician.fundraise_goal, 10000)

    def testPoliticianPersona(self):
        user = User.objects.create_user(username="brian")
        persona = Persona.objects.create(user=user, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        politician = Politician.objects.create(persona=persona, office_id=1, office_name="brian's office", fundraised=100, fundraise_goal=10000)
        address = toAddress(persona)
        norm_address = normalizeAddress(address)
        self.assertEqual(norm_address['line1'],'1111 deerfield drive')
        self.assertEqual(norm_address['city'],'Richmond')
        self.assertEqual(norm_address['state'],'VA')
        self.assertEqual(norm_address['zip'],'22911')
        self.assertEqual(politician.persona.num_followers,3)
        self.assertEqual(politician.persona.stage,2)