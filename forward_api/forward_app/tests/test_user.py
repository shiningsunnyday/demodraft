from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from forward_app.core_models import Persona
from forward_app.utils.civic import fetchAddress

"""
Tests for all functionality with Persona object
"""
class PersonaTest(TestCase):

    def testPersona(self):
        mainAccount = User.objects.create_user(username='mainAccount')
        follower = User.objects.create_user(username='follower1')
        mainpersona = Persona.objects.create(user=mainAccount, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        self.assertEqual(mainpersona.user,mainAccount)
        self.assertEqual(mainpersona.num_followers,3)
        self.assertEqual(mainpersona.line1,"1111 deerfield drive")
        self.assertEqual(mainpersona.city,"Richmond")
        self.assertEqual(mainpersona.state,"VA")
        self.assertEqual(mainpersona.zipcode,22911)


    def testFollowers(self):
        mainAccount = User.objects.create_user(username='mainAccount')
        follower1 = User.objects.create_user(username='follower1')
        follower2 = User.objects.create_user(username='follower2')
        follower3 = User.objects.create_user(username='follower3')       
        mainpersona = Persona.objects.create(user=mainAccount, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        mainpersona.users.add(follower1, follower2, follower3)
        follower1persona = Persona.objects.create(user=follower1, num_followers=1, stage=1, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        follower1persona.users.add(mainAccount)
        self.assertEqual(mainpersona.users.get(username=follower1),follower1)
        self.assertEqual(mainpersona.users.get(username=follower2),follower2)
        self.assertEqual(mainpersona.users.get(username=follower3),follower3)
        self.assertEqual(mainpersona.user, mainAccount)
        self.assertEqual(mainpersona.user.following.get(), follower1persona)


    def testcivicAPI(self):
        mainAccount = User.objects.create_user(username='mainAccount')
        mainpersona = Persona.objects.create(user=mainAccount, num_followers=3, stage=2, line1="2757 Fernleaf Rd", city="Charlottesville", state="VA", zipcode=22911)
        address = mainpersona.line1 + ' ' +mainpersona.city + ', ' +mainpersona.state + ' ' +str(mainpersona.zipcode)
        self.assertEqual(fetchAddress(address)['line1'],'2757 Fernleaf Road')
        self.assertEqual(fetchAddress(address)['city'],'Charlottesville')
        self.assertEqual(fetchAddress(address)['state'],'VA')
        self.assertEqual(fetchAddress(address)['zip'],'22911')







