from rest_framework.parsers import JSONParser
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser


class Meta(object):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    parser_classes = [JSONParser]