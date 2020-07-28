from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from forward_app.core_models import Persona

"""
Tests for all functionality with User object
"""
class UserTest(TestCase):

    def setUp(self):
        User.objects.create_user(email='librian2000@gmail.com', username='brian', password='pass')
        User.objects.create_user(email='msun@gmail.com', username='msun', password='stanford')
        User.objects.create_user(email='admin@demodraft.com', username='admin', passowrd='adminpass')

    def testName(self):
        user1 = User.objects.get_by_natural_key(username='brian')
        user2 = User.objects.get_by_natural_key(username='msun')
        user3 = User.objects.get_by_natural_key(username='admin')
        self.assertEqual(user1.username,'brian')
        self.assertEqual(user2.username,'msun')
        self.assertEqual(user3.username,'admin')

    def testEmail(self):
        user1 = User.objects.get_by_natural_key(username='brian')
        user2 = User.objects.get_by_natural_key(username='msun')
        user3 = User.objects.get_by_natural_key(username='admin')
        self.assertEqual(user1.email,"librian2000@gmail.com")
        self.assertEqual(user2.email,"msun@gmail.com")
        self.assertEqual(user3.email,'admin@demodraft.com')

    def testPersona(self):
        user1 = User.objects.get_by_natural_key(username='brian')
        user2 = User.objects.get_by_natural_key(username='msun')
        persona1 = Persona.objects.create(user=user1, followers=10, status='running 4 prez')
        persona2 = Persona.objects.create(user=user2, followers=5000, status='hello')
        persona1.users.add(user1)
        persona2.users.add(user2)
        self.assertEquals(persona1.followers, 10)
        self.assertEqual(persona1.status, 'running 4 prez')
        self.assertEquals(persona2.followers, 5000)
        self.assertEqual(persona2.status, 'hello')




    


    