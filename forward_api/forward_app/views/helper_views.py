from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress, merge
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *
from django.core.mail import EmailMessage
from django.conf import settings


class Address(APIView, Meta):
    @staticmethod
    def user_exists(username, password=None):
        filtered = User.objects.filter(username=username)
        return filtered.exists()

    def get(self, request):
        if set(request.GET.keys()) != {"username"}:
            return Response("Please provide username.", status=status.HTTP_400_BAD_REQUEST)
        if Address.user_exists(username=request.GET["username"]):
            user = User.objects.get(username=request.GET["username"])
            persona = user.persona
            sz = AddressSerializer(persona)
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if set(request.data.keys()) != {"username", "password", "address"}:
            return Response("Please provide username and address.", status=status.HTTP_400_BAD_REQUEST)
        user_creds = {"username": request.data["username"], "password": request.data["password"]}
        if Address.user_exists(**user_creds):
            user = User.objects.get(**user_creds)
            norm_address = normalizeAddress(request.data["address"])
            persona = user.persona
            # Should serialize this soon
            persona.line1 = norm_address['line1']
            persona.city = norm_address['city']
            persona.state = norm_address['state']
            persona.zipcode = norm_address['zip']
            positions = fetchPositions(request.data["address"])
            persona.save()
            return Response(positions, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)


class PoliticianV(APIView, Meta):
    def post(self, request):
        if set(request.data.keys()) != {"username", "scope", "index"}:
            return Response("Please provide username, one of local/state/country and index.",
                            status=status.HTTP_400_BAD_REQUEST)
        username = request.data["username"]
        if Address.user_exists(username):
            user = User.objects.get(username=username)
            persona = user.persona
            address = toAddress(persona)
            positions = fetchPositions(address, indices=True)
            if request.data['scope'] not in {"state", "local", "country"}:
                return Response("Scope must be one of \"local\", \"state\", or \"country\".",
                                status=status.HTTP_400_BAD_REQUEST)
            pos = positions[request.data['scope']][int(request.data['index'])]
            if Politician.objects.filter(persona=persona).exists():
                pol = Politician.objects.get(persona=persona)
                pol.office_id = pos['id']
                pol.name = pos['name']
                pol.save()
            else:
                pol = Politician(persona=persona, office_id=pos['id'], name=pos['name'])
                pol.save()
                Constituency.objects.create(politician=pol)
            user_info = UserSerializer(user)
            pol_info = PoliticianSerializer(pol)
            data = merge(user_info.data, pol_info.data)
            email = EmailMessage('New Politician: ' + user.username + ' registered!', 'Email: ' + user.email
                                 + '\nPosition: ' + pos['name'], settings.EMAIL_HOST_USER, ['demodraftapp@gmail.com'])
            email.fail_silently = False
            email.send()
            return Response(data, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Staff-only view that approves a politician using the account's username and preferred first and last names.
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if set(request.data.keys()) != {"username", "first", "last"}:
            return Response("Please provide username, first name and last name.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not Address.user_exists(request.data['username']):
            return Response("Username doesn't exist.", status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.data['username'])
        persona = user.persona
        persona.stage = 3
        pol = persona.politician
        if pol.approved:
            sz = PoliticianSerializer(pol)
            return Response(sz.data, status=status.HTTP_200_OK)
        pol.approved = True
        pol.first = request.data["first"]
        pol.last = request.data["last"]
        camp = Campaign(politician=pol)
        persona.save()
        pol.save()
        camp.save()
        sz = PoliticianSerializer(pol)
        return Response(sz.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        # Staff-only view that gets public info of politician for politician card
        if set(request.GET.keys()) == {"politician_id"}:
            pol = Politician.objects.get(id=int(request.GET['politician_id']))
            # serializes campaign info available to public
            camp_sz = CampaignSerializer(pol.campaign)
            pol_sz = PoliticianSerializer(pol)
            data = merge(pol_sz.data, camp_sz.data)
        elif set(request.GET.keys()) == set():
            sz = PoliticianSerializer(Politician.objects.filter(approved=True), many=True)
            data = sz.data
        else:
            sz = PoliticianSerializer(Politician.objects.all(), many=True)
            data = sz.data
        return Response(data, status=status.HTTP_200_OK)


class CampaignV(APIView, Meta):
    camp_attrs = {'actblue', 'fundraise_goal'}

    def get(self, request):
        # Staff-only view that gets public and customizable info of politician under personal campaign
        if set(request.GET.keys()) != {"politician_id"}:
            return Response("Please provide politician id.", status=status.HTTP_400_BAD_REQUEST)
        pol = Politician.objects.get(id=int(request.GET['politician_id']))
        camp = pol.campaign
        # serializes both campaign's public and customizable info
        sz = MyCampaignSerializer(camp)
        return Response(sz.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Updates customizable info for personal campaign
        if "politician_id" not in set(request.data):
            return Response("Please provide politician id.", status=status.HTTP_400_BAD_REQUEST)
        pol = Politician.objects.get(id=int(request.data['politician_id']))
        camp = pol.campaign
        for attr in CampaignV.camp_attrs:
            if attr in request.data:
                setattr(camp, attr, request.data[attr])
        camp.save()
        sz = MyCampaignSerializer(camp)
        return Response(sz.data, status=status.HTTP_200_OK)