from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Websites, Categories, Products, Groups, Options, Banners, Contacts
from decimal import *


# TODO: Test ShowProduct view

class InitialDataTest(TestCase):
    """
    Register necessary initial data for the tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.website = Websites.objects.create(url='store', title="Store Test")

        cls.cars = Categories.objects.create(websites=cls.website, title="Cars", position=1)
        cls.computers = Categories.objects.create(websites=cls.website, title="Computers", position=2)
        cls.books = Categories.objects.create(websites=cls.website, title="Books", position=4)
        cls.foods = Categories.objects.create(websites=cls.website, title="Foods", position=3)

        cls.products = (
            ("CyberpowerPC Gamer Supreme Liquid Cool Gaming PC, AMD Ryzen 7 3800X 3.9GHz, Radeon RX 5700 XT 8GB, 16GB\
             DDR4, 1TB NVMe SSD, WiFi & Win 10 Home (SLC8260A3)", 1229.99),
            ("Dell XPS 8930 Desktop i7-8700 16GB DDR4 Memory, 512GB SSD + 1TB SATA Hard Drive, 8GB Nvidia GeForce GTX\
             1080, DVD Burner, Windows 10 Pro, Black (Renewed)", 1499.66),
            ("Dell P2RF6 OptiPlex 5050 Small Form Factor Desktop, Intel Core i5-7500, 8GB RAM, 128GB SSD, Black \
            (Renewed)", 539.00),
            ("SkyTech Blaze II Gaming Computer PC Desktop – Ryzen 5 2600 6-Core 3.4 GHz, NVIDIA GeForce GTX 1660 6G, \
            500G SSD, 8GB DDR4, RGB, AC WiFi, Windows 10 Home 64-bit", 749.99),
            ("2012 CR-V LX Honda", 12998), ("2019 4Runner SR5 ", 33998), ("2019 Highlander Limited Toyota", 40998),
            ("2021 BMW 7-Series", 91463), ("2021 Aston Martin DBX", 176900), ("2021 Lamborghini Urus", 218009),
            ("I Love You to the Moon and Back Board book", 2), ("Chicka Chicka Boom Boom (Board Book)", 4.59),
            ("The Very Hungry Caterpillar Board book", 0.94), ("Brown Bear, Brown Bear, What Do You See?", 5),
            ("Meals", 115), ("Variety Rice", 45), ("Plain basbathi fried rice", 165), ("Veg.pulao", 160),
                    )

        for product in cls.products:
            Products.objects.create(websites=cls.website, categories=cls.computers,
                                    title=product[0], price=product[1])

        Contacts.objects.create(websites=cls.website, telephone="9999999999", email='example@email.com',
                                facebook='example', instagram='example', twitter='example')


class ShowProductsViewTest(InitialDataTest):

    def test_connection_success(self):

        response = self.client.get('/store/')

        self.assertEqual(response.status_code, 200)

    def test_connection_404(self):

        response = self.client.get('/store2/')

        self.assertEqual(response.status_code, 404)

    def test_context_website(self):

        response = self.client.get('/store/')
        context = response.context

        self.assertEqual(context['website'].title, "Store Test")

        self.assertEqual(context['categories'][0].title, "Cars")
        self.assertEqual(context['categories'][1].title, "Computers")
        self.assertEqual(context['categories'][2].title, "Foods")
        self.assertEqual(context['categories'][3].title, "Books")

        for x, product in enumerate(context['products']):
            self.assertEqual(product.title, self.products[x][0])
            self.assertEqual(product.price, Decimal(str(self.products[x][1])))

    def test_templates_name(self):

        response = self.client.get('/store/')
        templates = response.templates

        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")
        self.assertEqual(templates[7].name, "partial/_contact.html")
        self.assertEqual(templates[8].name, "partial/_credits.html")

    def test_content(self):

        response = self.client.get('/store/')

        self.assertContains(response, "example@email.com")
        self.assertContains(response, "9999999999")
        self.assertContains(response, "facebook.com/example")
        self.assertContains(response, "instagram.com/example")
        self.assertContains(response, "twitter.com/example")
