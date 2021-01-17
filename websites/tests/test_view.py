from django.test import TestCase, Client
from websites.utils.utils import money_format
from ..models import Websites, Contacts, Categories, Products, Groups, Options
from decimal import *

# TestCase self.client hasn't get method


class WebsiteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.website = Websites.objects.create(url='website', title="Website")

    def test_incorrect_url(self):

        client = Client()

        response = client.get('/Website/')
        self.assertEqual(response.status_code, 404)

        response = client.get('/websites/')
        self.assertEqual(response.status_code, 404)

    def test_website(self):
        """
        Using the correct url check status, context, templates names, and html code
        """

        client = Client()

        response = client.get('/website/')

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, "Website")
        self.assertEqual(context['icon'], None)
        self.assertEqual(context['color'], None)
        self.assertEqual(context['contact'], None)
        self.assertEqual(context['categories'].exists(), False)
        self.assertEqual(context['products'].exists(), False)

        templates = response.templates
        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, "partial/_credits.html")

        self.assertContains(response, "Website")

    def test_contact(self):
        """
        Register a contact for the website and check status, context, templates, and html code
        """

        Contacts.objects.create(websites=self.website, telephone='7873923408', email='example@email.com',
                                facebook='example', instagram='example', twitter='example', linkedin='example',
                                whatsapp='7873923408')

        client = Client()

        response = client.get('/website/')

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['contact'].telephone, '7873923408')
        self.assertEqual(context['contact'].email, 'example@email.com')
        self.assertEqual(context['contact'].facebook, 'example')
        self.assertEqual(context['contact'].instagram, 'example')
        self.assertEqual(context['contact'].twitter, 'example')
        self.assertEqual(context['contact'].linkedin, 'example')
        self.assertEqual(context['contact'].whatsapp, '7873923408')

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_contact.html')
        self.assertEqual(templates[5].name, 'partial/_credits.html')

        self.assertContains(response, "Website")
        self.assertContains(response, "example@email.com")
        self.assertContains(response, "7873923408")
        self.assertContains(response, "facebook.com/example")
        self.assertContains(response, "instagram.com/example")
        self.assertContains(response, "twitter.com/example")
        self.assertContains(response, "linkedin.com/in/example")

    def test_categories(self):
        """
        Register categories and check status, context, templates, html code
        """

        Categories.objects.create(websites=self.website, title="Category 1", position=1)
        Categories.objects.create(websites=self.website, title="Category 2", position=2)
        Categories.objects.create(websites=self.website, title="Category 3", position=4)
        Categories.objects.create(websites=self.website, title="Category 4", position=3)

        client = Client()

        response = client.get('/website/')

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")
        self.assertEqual(context['categories'][2].title, "Category 4")
        self.assertEqual(context['categories'][3].title, "Category 3")

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_credits.html')

        self.assertContains(response, "Category 1")
        self.assertContains(response, "Category 2")
        self.assertContains(response, "Category 3")
        self.assertContains(response, "Category 4")


class ShowProductsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.website = Websites.objects.create(url='website', title="Website")

        cls.c1 = Categories.objects.create(websites=cls.website, title="Category 1", position=1)
        cls.c2 = Categories.objects.create(websites=cls.website, title="Category 2", position=2)

        cls.products = (
            ("Product One", 10.2), ("Product Two", 10.2), ("Product Three", 10.2), ("Product Four", 10.2),
            ("Product Five", 10.2), ("Product Six", 10.2), ("Product Seven", 10.2), ("Product Eight", 10.2),
        )

        for product in cls.products:
            Products.objects.create(websites=cls.website, categories=cls.c1, title=product[0], price=product[1])

        Products.objects.create(websites=cls.website, categories=cls.c1, title="Promotional", price=10.2,
                                promotional_price=5, position=9)

        cls.products2 = (
            ("One Product", 10.2), ("Two Product", 10.2), ("Three Product", 10.2), ("Four Product", 10.2),
            ("Five Product", 10.2), ("Six Product", 10.2), ("Seven Product", 10.2), ("Eight Product", 10.2),
        )

        for product in cls.products2:
            Products.objects.create(websites=cls.website, categories=cls.c2, title=product[0], price=product[1],
                                    show_on_home=False)

        Products.objects.create(websites=cls.website, categories=cls.c2, title="Promotional2", price=10.2,
                                promotional_price=5, show_on_home=False)

    def test_products_on_home(self):

        client = Client()

        response = client.get('/website/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")

        for x, product in enumerate(context['products']):

            self.assertEqual(product.title, self.products[x][0])
            self.assertEqual(product.price, Decimal(str(self.products[x][1])))

            self.assertContains(response, self.products[x][0])
            money = money_format(self.products[x][1], self.website.currency, self.website.language)
            self.assertContains(response, money)

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")
        self.assertEqual(templates[7].name, 'partial/_credits.html')

    def test_products_on_home_page_2(self):

        client = Client()

        response = client.get('/website/?page=2')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")

        self.assertEqual(context['products'][0].title, "Promotional")
        self.assertEqual(context['products'][0].price, Decimal(str(10.2)))
        self.assertEqual(context['products'][0].promotional_price, Decimal(str(5)))

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, 'partial/_pagination.html')
        self.assertEqual(templates[7].name, 'partial/_credits.html')

        self.assertContains(response, "Promotional")
        money = money_format(10.2, self.website.currency, self.website.language)
        self.assertContains(response, money)
        money = money_format(5, self.website.currency, self.website.language)
        self.assertContains(response, money)

    def test_products_by_category(self):

        client = Client()

        response = client.get('/website/c/category-2/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")

        for x, product in enumerate(context['products']):

            self.assertEqual(product.title, self.products2[x][0])
            self.assertEqual(product.price, Decimal(str(self.products2[x][1])))

            self.assertContains(response, self.products2[x][0])
            money = money_format(self.products2[x][1], self.website.currency, self.website.language)
            self.assertContains(response, money)

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")
        self.assertEqual(templates[7].name, 'partial/_credits.html')

    def test_products_by_category_page_2(self):

        client = Client()

        response = client.get('/website/c/category-2/?page=2')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")

        self.assertEqual(context['products'][0].title, "Promotional2")
        self.assertEqual(context['products'][0].price, Decimal('10.2'))
        self.assertEqual(context['products'][0].promotional_price, Decimal('5'))

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, 'partial/_pagination.html')
        self.assertEqual(templates[7].name, 'partial/_credits.html')

        self.assertContains(response, "Promotional2")
        money = money_format(10.2, self.website.currency, self.website.language)
        self.assertContains(response, money)
        money = money_format(5, self.website.currency, self.website.language)
        self.assertContains(response, money)

    def test_category_error_404(self):

        client = Client()

        response = client.get('/website/c/category-3/')

        self.assertEqual(response.status_code, 404)

    def test_products_by_search(self):

        client = Client()

        response = client.get('/website/?search=One')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")

        self.assertEqual(context['products'][0].title, "Product One")
        self.assertEqual(context['products'][0].price, Decimal('10.2'))

        self.assertEqual(context['products'][1].title, "One Product")
        self.assertEqual(context['products'][1].price, Decimal('10.2'))

        templates = response.templates
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, 'partial/_pagination.html')
        self.assertEqual(templates[7].name, 'partial/_credits.html')

        self.assertContains(response, "Product One")
        self.assertContains(response, "One Product")
        money = money_format(10.2, self.website.currency, self.website.language)
        self.assertContains(response, money)


def create_product_with_group(website, category, price_type, price=None, option_price=None, group_price_type=None):

    product = Products.objects.create(websites=website, categories=category, title='Product',
                                      price=price, price_type=price_type)

    radio = Groups.objects.create(websites=website, products=product, title="radio group",
                                  maximum=1, minimum=1, price_type=group_price_type)
    checkbox = Groups.objects.create(websites=website, products=product, title="checkbox group",
                                     maximum=1, minimum=0, price_type=group_price_type)
    numbers = Groups.objects.create(websites=website, products=product, title="numbers group",
                                    maximum=10, minimum=0, price_type=group_price_type)

    Options.objects.create(websites=website, groups=radio, title="Op1", price=option_price)
    Options.objects.create(websites=website, groups=radio, title="Op2", price=option_price)
    Options.objects.create(websites=website, groups=radio, title="Op3", price=option_price)
    Options.objects.create(websites=website, groups=radio, title="Readonly", maximum=1, minimum=1,
                           price=option_price)

    Options.objects.create(websites=website, groups=checkbox, title="Op1", price=option_price)
    Options.objects.create(websites=website, groups=checkbox, title="Op2", price=option_price)
    Options.objects.create(websites=website, groups=checkbox, title="Op3", price=option_price)
    Options.objects.create(websites=website, groups=checkbox, title="Readonly", maximum=1, minimum=1,
                           price=option_price)

    Options.objects.create(websites=website, groups=numbers, title="Op1", maximum=5, minimum=0, price=option_price)
    Options.objects.create(websites=website, groups=numbers, title="Op2", maximum=5, minimum=0, price=option_price)
    Options.objects.create(websites=website, groups=numbers, title="Op3", maximum=5, minimum=0, price=option_price)
    Options.objects.create(websites=website, groups=numbers, title="Readonly", maximum=5, minimum=5,
                           price=option_price)


class ShowProductViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.website = Websites.objects.create(url='website', title="Website")
        cls.category = Categories.objects.create(websites=cls.website, title="Category")

    def test_product_404(self):

        client = Client()

        response = client.get('/website/p/product-404/')

        self.assertEqual(response.status_code, 404)

    def test_product_200(self):

        Products.objects.create(websites=self.website, categories=self.category, title='Product',
                                price=10, price_type='1')

        client = Client()

        response = client.get('/website/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, self.website.title)
        self.assertEqual(context['icon'], None)
        self.assertEqual(context['color'], None)
        self.assertEqual(context['contact'], None)
        self.assertEqual(context['categories'][0].title, "Category")
        self.assertEqual(context['product'].title, "Product")

        templates = response.templates
        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_product.html')
        self.assertEqual(templates[6].name, "partial/_credits.html")

    def test_price_type_1(self):

        create_product_with_group(self.website, self.category, '1', 30000)

        client = Client()

        response = client.get('/website/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['groups'][0].title, "radio group")
        self.assertEqual(context['groups'][1].title, "checkbox group")
        self.assertEqual(context['groups'][2].title, "numbers group")

        self.assertEqual(context['options'][0].title, "Op1")
        self.assertEqual(context['options'][0].maximum, 1)
        self.assertEqual(context['options'][0].minimum, 0)
        self.assertEqual(context['options'][1].title, "Op2")
        self.assertEqual(context['options'][1].maximum, 1)
        self.assertEqual(context['options'][1].minimum, 0)
        self.assertEqual(context['options'][2].title, "Op3")
        self.assertEqual(context['options'][2].maximum, 1)
        self.assertEqual(context['options'][2].minimum, 0)
        self.assertEqual(context['options'][3].title, "Readonly")
        self.assertEqual(context['options'][3].maximum, 1)
        self.assertEqual(context['options'][3].minimum, 1)

        self.assertEqual(context['options'][4].title, "Op1")
        self.assertEqual(context['options'][4].maximum, 1)
        self.assertEqual(context['options'][4].minimum, 0)
        self.assertEqual(context['options'][5].title, "Op2")
        self.assertEqual(context['options'][5].maximum, 1)
        self.assertEqual(context['options'][5].minimum, 0)
        self.assertEqual(context['options'][6].title, "Op3")
        self.assertEqual(context['options'][6].maximum, 1)
        self.assertEqual(context['options'][6].minimum, 0)
        self.assertEqual(context['options'][7].title, "Readonly")
        self.assertEqual(context['options'][7].maximum, 1)
        self.assertEqual(context['options'][7].minimum, 1)

        self.assertEqual(context['options'][8].title, "Op1")
        self.assertEqual(context['options'][8].maximum, 5)
        self.assertEqual(context['options'][8].minimum, 0)
        self.assertEqual(context['options'][9].title, "Op2")
        self.assertEqual(context['options'][9].maximum, 5)
        self.assertEqual(context['options'][9].minimum, 0)
        self.assertEqual(context['options'][10].title, "Op3")
        self.assertEqual(context['options'][10].maximum, 5)
        self.assertEqual(context['options'][10].minimum, 0)
        self.assertEqual(context['options'][11].title, "Readonly")
        self.assertEqual(context['options'][11].maximum, 5)
        self.assertEqual(context['options'][11].minimum, 5)

    def test_price_type_2(self):

        create_product_with_group(self.website, self.category, '2', 30000, 200, '1')

        client = Client()

        response = client.get('/website/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['groups'][0].title, "radio group")
        self.assertEqual(context['groups'][1].title, "checkbox group")
        self.assertEqual(context['groups'][2].title, "numbers group")

        self.assertEqual(context['options'][0].title, "Op1")
        self.assertEqual(context['options'][0].maximum, 1)
        self.assertEqual(context['options'][0].minimum, 0)
        self.assertEqual(context['options'][1].title, "Op2")
        self.assertEqual(context['options'][1].maximum, 1)
        self.assertEqual(context['options'][1].minimum, 0)
        self.assertEqual(context['options'][2].title, "Op3")
        self.assertEqual(context['options'][2].maximum, 1)
        self.assertEqual(context['options'][2].minimum, 0)
        self.assertEqual(context['options'][3].title, "Readonly")
        self.assertEqual(context['options'][3].maximum, 1)
        self.assertEqual(context['options'][3].minimum, 1)

        self.assertEqual(context['options'][4].title, "Op1")
        self.assertEqual(context['options'][4].maximum, 1)
        self.assertEqual(context['options'][4].minimum, 0)
        self.assertEqual(context['options'][5].title, "Op2")
        self.assertEqual(context['options'][5].maximum, 1)
        self.assertEqual(context['options'][5].minimum, 0)
        self.assertEqual(context['options'][6].title, "Op3")
        self.assertEqual(context['options'][6].maximum, 1)
        self.assertEqual(context['options'][6].minimum, 0)
        self.assertEqual(context['options'][7].title, "Readonly")
        self.assertEqual(context['options'][7].maximum, 1)
        self.assertEqual(context['options'][7].minimum, 1)

        self.assertEqual(context['options'][8].title, "Op1")
        self.assertEqual(context['options'][8].maximum, 5)
        self.assertEqual(context['options'][8].minimum, 0)
        self.assertEqual(context['options'][9].title, "Op2")
        self.assertEqual(context['options'][9].maximum, 5)
        self.assertEqual(context['options'][9].minimum, 0)
        self.assertEqual(context['options'][10].title, "Op3")
        self.assertEqual(context['options'][10].maximum, 5)
        self.assertEqual(context['options'][10].minimum, 0)
        self.assertEqual(context['options'][11].title, "Readonly")
        self.assertEqual(context['options'][11].maximum, 5)
        self.assertEqual(context['options'][11].minimum, 5)

