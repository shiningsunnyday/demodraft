from forward_app.utils.civic import fetchPositions, normalizeAddress, toAddress, merge
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .meta import Meta
from forward_app.serializers import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# from forward_app.utils.Google import Create_Service
# import base64
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


class Address(APIView, Meta):

    @staticmethod
    def user_exists(username, password=None):
        filtered = User.objects.filter(username=username)
        if password:
            filtered = filtered.filter(password=password)
        return filtered.exists()

    def get(self, request):
        if set(request.data.keys()) != {"username", "password"}:
            return Response("Please provide username and password.", status=status.HTTP_400_BAD_REQUEST)
        username, password = request.data["username"], request.data["password"]
        if Address.user_exists(username, password):
            user = User.objects.get(username=username, password=password)
            persona = user.persona
            address = {}
            address['line1'] = persona.line1
            address['city'] = persona.city
            address['state'] = persona.state
            address['zip'] = persona.zipcode
            return Response(address, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if set(request.data.keys()) != {"username", "password", "address"}:
            return Response("Please provide username and address.", status=status.HTTP_400_BAD_REQUEST)
        username, password = request.data["username"], request.data["password"]
        if Address.user_exists(username, password):
            user = User.objects.get(username=username, password=password)
            norm_address = normalizeAddress(request.data["address"])
            persona = user.persona
            persona.line1 = norm_address['line1']
            persona.city = norm_address['city']
            persona.state = norm_address['state']
            persona.zipcode = norm_address['zip']
            persona.save()
            positions = fetchPositions(request.data["address"])
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
            else:
                pol = Politician(persona=persona, office_id=pos['id'], name=pos['name'])
            pol.save()
            data = merge(UserSerializer(user).data, PoliticianSerializer(pol).data)

            # email = EmailMessage(
            # 'New Politician: ' + user.username + ' registered!', 'Email: '+user.email+ '\nPosition: '+pos['name'], settings.EMAIL_HOST_USER, ['demodraftapp@gmail.com']
            # )
            # email.fail_silently = False
            # email.send()

            # service = Create_Service(settings.CLIENT_SECRET_FILE, settings.API_NAME, settings.API_VERSION, settings.SCOPES) 
            # emailMsg = 'New Politician: ' + user.username + ' registered!', 'Email: '+user.email+ '\nPosition: '+pos['name']
            # mimeMessage = MIMEMultipart()
            # mimeMessage['to'] = 'demodraftapp@gmail.com'
            # mimeMessage['subject'] = 'New Politician ' + user.username + " Registered!"
            # mimeMessagge.attach(MIMEText(emailMsg,"plain"))
            # raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            # message = service.users().messages().send(userID='me', body={'raw': raw_string}).execute()

            return Response(data, status=status.HTTP_200_OK)
        return Response("Username or password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if set(request.data.keys()) != {"username", "password", "first", "last"}:
            return Response("Please provide username, password, first name and last name.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not Address.user_exists(request.data['username'], password=request.data['password']):
            return Response("Either username or password is wrong.", status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.data['username'])
        persona = user.persona
        pol = persona.politician
        if pol.approved:
            sz = PoliticianSerializer(pol)
            return Response(sz.data, status=status.HTTP_200_OK)
        pol.approved = True
        pol.first = request.data["first"]
        pol.last = request.data["last"]
        camp = Campaign(politician=pol)
        pol.save()
        camp.save()
        sz = PoliticianSerializer(pol)
        return Response(sz.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        if set(request.GET.keys()) == {"politician_id"}:
            pol = Politician.objects.get(id=int(request.GET['politician_id']))
            sz = CampaignSerializer(pol.campaign)
        elif set(request.GET.keys()) == set():
            sz = PoliticianSerializer(Politician.objects.filter(approved=True), many=True)
        else:
            sz = PoliticianSerializer(Politician.objects.all(), many=True)
        return Response(sz.data, status=status.HTTP_200_OK)


class CampaignV(APIView, Meta):
    camp_attrs = {'actblue', 'fundraise_goal'}

    def get(self, request):
        if set(request.GET.keys()) != {"politician_id"}:
            return Response("Please provide politician id.", status=status.HTTP_400_BAD_REQUEST)
        pol = Politician.objects.get(id=int(request.GET['politician_id']))
        camp = pol.campaign
        sz = MyCampaignSerializer(camp)
        return Response(sz.data, status=status.HTTP_200_OK)

    def put(self, request):
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