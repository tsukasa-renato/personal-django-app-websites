from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class WebistesTests(APITestCase):

    def create_website(self):
        """
        Creating a website using the API
        """

        url = reverse('websites:websites-list')
        data = {'url': 'website', 'title': 'Website'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
