from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from forward_app.core_models import Persona

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
        mainpersona.save()
        mainpersona.users.add(follower1, follower2, follower3)
        follower1persona = Persona.objects.create(user=follower1, num_followers=1, stage=1, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        follower1persona.save()
        follower1persona.users.add(mainAccount)
        # include queryset w all 3 followers -- replace follower1 below w this
        # self.assertEqual(mainpersona.users.all(),follower1)
        self.assertEqual(mainpersona.user, mainAccount)
        # self.assertEqual(list(mainpersona.user.followers.all()), follower1persona)
        for e in mainpersona.user.followers.all():
            self.assertEqual(e,follower1persona)

        self.assertEqual(follower1persona.users.all(),mainAccount)
        self.assertEqual(follower1persona.user, follower1)

    #For testing the models use the "normalizedInput" return value from the Google API, which can be accessed from the response json
    #Can be accessed r.json()['normalizedInput'] in the fetch method from utils/civic.py
    # def testCivicAPI(self):


    
