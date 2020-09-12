from django.test import TestCase
from forward_app.core_models import Politician, Stance, Persona, Policy, Plan, Step
from django.contrib.auth.models import User
from forward_app.utils.civic import normalizeAddress, toAddress


"""
Tests for all functionality with Politician object
"""
class PoliticianTest(TestCase):

    def testPolitician(self):
        user = User.objects.create_user(username="brian")
        persona = Persona.objects.create(user=user, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        politician = Politician.objects.create(persona=persona, office_id=1, name="brian's office")

        self.assertEqual(politician.office_id, 1)
        self.assertEqual(politician.name, "brian's office")

    def testPoliticianPersona(self):
        user = User.objects.create_user(username="brian")
        persona = Persona.objects.create(user=user, num_followers=3, stage=2, line1="1111 deerfield drive", city="Richmond", state="VA", zipcode=22911)
        politician = Politician.objects.create(persona=persona, office_id=1, name="brian's office")
        address = toAddress(persona)
        norm_address = normalizeAddress(address)
        self.assertEqual(norm_address['line1'],'1111 deerfield drive')
        self.assertEqual(norm_address['city'],'Richmond')
        self.assertEqual(norm_address['state'],'VA')
        self.assertEqual(norm_address['zip'],'22911')
        self.assertEqual(politician.persona.num_followers,3)
        self.assertEqual(politician.persona.stage,2)


class StancesTest(TestCase):
    def setUp(self):
        self.policy1 = Policy.objects.create(category=0, name='Universal Basic Income',
                                             statement='Universal Basic Income',
                                             description='Everyone gets 1000 dollars a month.')
        self.policy2 = Policy.objects.create(category=1, name='Universal Health Care', statement='Healthcare for all',
                                             description='We need to give medical services to all citizens.')
        user1 = User.objects.create_user(username="michaelsun1")
        user2 = User.objects.create_user(username="michaelsun2")
        persona1 = Persona.objects.create(user=user1)
        persona2 = Persona.objects.create(user=user2)
        self.politician1 = Politician.objects.create(persona=persona1)
        self.politician2 = Politician.objects.create(persona=persona2)

    def testGetStances(self):
        Stance.objects.create(politician=self.politician1, policy=self.policy1, message="Hell yes")
        Stance.objects.create(politician=self.politician1, policy=self.policy2, message="Hell no")
        stances = self.politician1.stance_set.all()
        self.assertEqual(stances[0].politician, self.politician1)
        self.assertEqual(stances[1].message, "Hell no")

    def testGetPoliticians(self):
        Stance.objects.create(politician=self.politician1, policy=self.policy1, message="Heck yea")
        Stance.objects.create(politician=self.politician2, policy=self.policy1, message="Heck yea too")
        politicians = self.policy1.politician_set.all()
        self.assertEqual(politicians[0], self.politician1)
        self.assertEqual(politicians[1].persona.user.username, "michaelsun2")

    def testGetPolicies(self):
        Stance.objects.create(politician=self.politician1, policy=self.policy1, message="Heck yea")
        Stance.objects.create(politician=self.politician2, policy=self.policy1, message="Heck yea too")
        Stance.objects.create(politician=self.politician1, policy=self.policy2, message="Hell no")
        Stance.objects.create(politician=self.politician2, policy=self.policy2, message="Hell no too")
        policies = self.politician1.policies.all()
        self.assertEqual(policies[0].name, "Universal Basic Income")

class PlanTest(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="brian1")
        user2 = User.objects.create_user(username="brian2")
        persona1 = Persona.objects.create(user=user1)
        persona2 = Persona.objects.create(user=user2)
        self.politician1 = Politician.objects.create(persona=persona1)
        self.politician2 = Politician.objects.create(persona=persona2)

    def testPlan(self):
        plan1 = Plan.objects.create(lead_step_id=0, politician=self.politician1, scope="state")
        plan2 = Plan.objects.create(lead_step_id=0, politician=self.politician2, scope="local")
        self.assertEquals(plan1.politician, self.politician1)
        self.assertEquals(plan2.politician, self.politician2)
        self.assertEqual(plan1.scope, "state")
        self.assertEqual(plan1.lead_step_id,0)


class StepTest(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="brian1")
        user2 = User.objects.create_user(username="brian2")
        persona1 = Persona.objects.create(user=user1)
        persona2 = Persona.objects.create(user=user2)
        self.politician1 = Politician.objects.create(persona=persona1)
        self.politician2 = Politician.objects.create(persona=persona2)

    def testStep(self):
        plan1 = Plan.objects.create(lead_step_id=3, politician=self.politician1, scope="state")
        step3 = Step.objects.create(plan = plan1, description="Meet with supporters")
        step2 = Step.objects.create(plan = plan1, next_step_id=step3.id, description="Ask for donations")
        step1 = Step.objects.create(plan = plan1, next_step_id=step2.id, description="Organize speeches")
        self.assertEquals(plan1.lead_step_id, step1.id)
        self.assertEqual(step1.next_step_id, step2.id)
        self.assertEqual(step2.next_step_id, step3.id)
        self.assertEqual(step1.plan, plan1)



