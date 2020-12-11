from django.test import TestCase
from django.db.utils import IntegrityError
from . import models


def create_website_for_test(url, title):
    return models.Websites.objects.create(url=url, title=title)


def create_category_for_test(website, title):
    return models.Categories.objects.create(websites=website, title=title)


class ProductsModelTest(TestCase):

    def test_register_product(self):
        """
        Test a common register
        """
        
        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")
        p1 = models.Products.objects.create(websites=w1, categories=c1, title="title", price=1)

        self.assertEqual(p1.id, 1)

    def test_unique_constraints(self):
        """
        Test unique constraints, register two products with same website and title (slug)
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")
        models.Products.objects.create(websites=w1, categories=c1, title="title", price=1)

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price=1)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_fail_in_check_price_without_price(self):
        """
        Test check price, register a product with price_type in (1,2,3) and price=None
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='1')
        self.assertEqual(ValueError, type(raised.exception))

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='2')
        self.assertEqual(ValueError, type(raised.exception))

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='3')
        self.assertEqual(ValueError, type(raised.exception))

    def test_fail_in_check_price_with_price(self):
        """
        Test check price, register a product with price_type in (4,5) and price=1
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='4', price=1)
        self.assertEqual(ValueError, type(raised.exception))

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='5', price=1)
        self.assertEqual(ValueError, type(raised.exception))

    def test_success_in_check_price_with_price(self):
        """
            Test check price, register a product with price_type in (1,2,3) and price=1
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='1', price=1, position=1)
        models.Products.objects.create(websites=w1, categories=c1, title="title2", price_type='2', price=1, position=2)
        models.Products.objects.create(websites=w1, categories=c1, title="title3", price_type='3', price=1, position=3)

        self.assertQuerysetEqual(models.Products.objects.all().order_by('position'),
                                 ['<Products: title>', '<Products: title2>', '<Products: title3>'])

    def test_success_in_check_price_without_price(self):
        """
            Test check price, register a product with price_type in (4,5) and price=None
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='4', position=1)
        models.Products.objects.create(websites=w1, categories=c1, title="title2", price_type='5', position=2)

        self.assertQuerysetEqual(models.Products.objects.all().order_by('position'),
                                 ['<Products: title>', '<Products: title2>'])

    def test_fail_in_check_promotional_price_without_price(self):
        """
            Test check promotional price, register a product without price, but with promotional price
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price_type='4', promotional_price=1)
        self.assertEqual(ValueError, type(raised.exception))

    def test_fail_in_check_promotional_price_with_price(self):
        """
            Test check promotional price, register a product with promotional price greater than price
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        with self.assertRaises(Exception) as raised:
            models.Products.objects.create(websites=w1, categories=c1, title="title", price=1, promotional_price=2)
        self.assertEqual(ValueError, type(raised.exception))

    def test_success_in_check_promotional_price(self):
        """
            Test check promotional price, register a product with promotional price
        """

        w1 = create_website_for_test('url', "title")
        c1 = create_category_for_test(w1, "title")

        models.Products.objects.create(websites=w1, categories=c1, title="title", price=2, promotional_price=1)

        self.assertQuerysetEqual(models.Products.objects.all().order_by('position'), ['<Products: title>'])
