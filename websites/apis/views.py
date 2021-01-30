from websites.models import Websites
from rest_framework import viewsets
from .serializers import WebsitesSerializer


class WebsitesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows websites to be viewed or edited.
    """
    queryset = Websites.objects.all().order_by('-created_at')
    serializer_class = WebsitesSerializer
