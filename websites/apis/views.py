from websites.models import Websites
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import WebsitesSerializer


class WebsitesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow websites to be viewed or edited
    """

    queryset = Websites.objects.all().order_by('pk')
    serializer_class = WebsitesSerializer
