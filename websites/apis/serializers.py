from rest_framework import serializers
from websites.models import Websites


class WebsitesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Websites
        fields = ['pk', 'url', 'title', 'home', 'timezone', 'currency', 'language']
