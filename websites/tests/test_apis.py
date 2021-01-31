from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class APIsTest(APITestCase):

    def setUp(self):

        self.credentials = {
            'username': 'admin',
            'password': 'PASSsecret123'
        }

        User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    def check_information(self, url, data, keys):
        """
        Tests POST and GET request with the {name-model}-list url
        """

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in keys:

            self.assertEqual(response.data[key], data[key])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in keys:

            self.assertEqual(data[key], response.data['results'][0][key])

    def test_list_url(self):
        """
        Tests POST and GET request with the websites-list url
        """

        url = reverse('websites:websites-list')
        data = {'url': 'website', 'title': 'website'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the colors-list url
        """

        url = reverse('websites:colors-list')
        data = {'websites': 1, 'navbar': 'ffffff', 'title': '000000'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the contacts-list url
        """

        url = reverse('websites:contacts-list')
        data = {'websites': 1, 'email': 'example@gmail.com', 'telephone': '7873923408'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the categories-list url
        """

        url = reverse('websites:categories-list')
        data = {'websites': 1, 'title': 'Category 1'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the products-list url
        """

        url = reverse('websites:products-list')
        data = {'websites': 1, 'categories': 1, 'title': 'Product 1', 'price': '300.20'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the groups-list url
        """

        url = reverse('websites:groups-list')
        data = {'websites': 1, 'products': 1, 'title': 'Group 1'}

        self.check_information(url, data, data.keys())

        """
        Tests POST and GET request with the options-list url
        """

        url = reverse('websites:options-list')
        data = {'websites': 1, 'groups': 1, 'title': 'Option 1'}

        self.check_information(url, data, data.keys())
