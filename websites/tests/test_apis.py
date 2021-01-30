from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WebsitesTest(APITestCase):

    def test_create_websites(self):
        """
        Create a website using API
        """

        url = reverse('websites:websites-list')
        data = {'url': 'website', 'title': 'website'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
