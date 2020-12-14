from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import Websites, Categories, Products


class ProductsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.website = Websites.objects.create(url='url', title="title")
        cls.category = Categories.objects.create(websites=cls.website, title="title")

    def test_register_product(self):
        """
        Test a common register
        """

        p = Products.objects.create(websites=self.website, categories=self.category, title="title", price=1)

        self.assertEqual(p.id, 1)

    def test_unique_constraints(self):
        """
        Register two products with same website and title (slug)
        """

        Products.objects.create(websites=self.website, categories=self.category, title="title", price=1)

        with self.assertRaises(Exception):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price=1)

    def test_fail_in_check_price_without_price(self):
        """
        Register a product with price_type in (1,2,3) and price=None
        """

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='1')

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='2')

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='3')

    def test_fail_in_check_price_with_price(self):
        """
        Register a product with price_type in (4,5) and price=1
        """

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='4',
                                    price=1)

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='5',
                                    price=1)

    def test_success_in_check_price_with_price(self):
        """
        Register a product with price_type in (1,2,3) and price=1
        """

        Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='1',
                                price=1, position=1)
        Products.objects.create(websites=self.website, categories=self.category, title="title2", price_type='2',
                                price=1, position=2)
        Products.objects.create(websites=self.website, categories=self.category, title="title3", price_type='3',
                                price=1, position=3)

        self.assertQuerysetEqual(Products.objects.all().order_by('position'),
                                 ['<Products: title>', '<Products: title2>', '<Products: title3>'])

    def test_success_in_check_price_without_price(self):
        """
        Register a product with price_type in (4,5) and price=None
        """

        Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='4',
                                position=1)
        Products.objects.create(websites=self.website, categories=self.category, title="title2", price_type='5',
                                position=2)

        self.assertQuerysetEqual(Products.objects.all().order_by('position'),
                                 ['<Products: title>', '<Products: title2>'])

    def test_fail_in_check_promotional_price_without_price(self):
        """
        Register a product without price, but with promotional price
        """

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price_type='4',
                                    promotional_price=1)

    def test_fail_in_check_promotional_price_with_price(self):
        """
        Register a product with promotional price greater than price
        """

        with self.assertRaises(ValueError):
            Products.objects.create(websites=self.website, categories=self.category, title="title", price=1,
                                    promotional_price=2)

    def test_success_in_check_promotional_price(self):
        """
        Register a product with promotional price
        """

        Products.objects.create(websites=self.website, categories=self.category, title="title", price=2,
                                promotional_price=1)

        self.assertQuerysetEqual(Products.objects.all().order_by('position'), ['<Products: title>'])
