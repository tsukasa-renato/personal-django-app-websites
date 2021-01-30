from websites.models import Websites
from rest_framework import serializers


class WebsitesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Websites
        fields = ['pk', 'url', 'title', 'home', 'timezone', 'currency', 'language']
