from rest_framework import viewsets
from websites.models import Websites
from .serializers import WebsitesSerializer


class WebsitesViewSet(viewsets.ModelViewSet):
    """
    API to view and edit the websites
    """

    queryset = Websites.objects.all().order_by('-created_at')
    serializer_class = WebsitesSerializer
