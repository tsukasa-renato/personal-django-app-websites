from django.test import TestCase, Client
from websites.utils.utils import money_format
from ..models import Websites
from decimal import Decimal
from .scenarios import check_info, colors, images, products, product_type

# BUG: TestCase self.client hasn't get method

"""
For the tests with the views, we'll check the status code, context sent, template name rendered, HTML content.
"""


class WebsiteTest(TestCase):

    def test_url(self):

        client = Client()

        Websites.objects.create(url='testurl', title="Test Url")

        response = client.get('/Test Url/')
        self.assertEqual(response.status_code, 404)

        """
        # In mysql this test fails, because mysql is non-sensitive.
        response = client.get('/TESTURL/')
        self.assertEqual(response.status_code, 404)
        """

        response = client.get('/testurl1/')
        self.assertEqual(response.status_code, 404)

        response = client.get('/testurl/')
        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, "Test Url")
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

        self.assertContains(response, "Test Url")

    def test_check_info(self):

        check_info()

        client = Client()

        response = client.get('/checkinfo/')
        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, "Check Info")
        self.assertEqual(context['contact'].telephone, '7873923408')
        self.assertEqual(context['contact'].email, 'checkinfo@gmail.com')
        self.assertEqual(context['contact'].facebook, 'checkinfofacebook')
        self.assertEqual(context['contact'].instagram, 'checkinfoinstagram')
        self.assertEqual(context['contact'].twitter, 'checkinfotwitter')
        self.assertEqual(context['contact'].linkedin, 'checkinfolinkedin')
        self.assertEqual(context['contact'].pinterest, 'checkinfopinterest')
        self.assertEqual(context['contact'].youtube, 'checkinfoyoutube')
        self.assertEqual(context['contact'].whatsapp, '7873923408')
        self.assertEqual(context['contact'].social_media_text, 'Follow us :D')
        self.assertEqual(context['contact'].whatsapp_text, 'Whatsapp:')
        self.assertEqual(context['categories'][0].title, "Category 1")
        self.assertEqual(context['categories'][1].title, "Category 2")
        self.assertEqual(context['categories'][2].title, "Category 3")
        self.assertEqual(context['categories'][3].title, "Category 4")
        self.assertEqual(context['categories'][4].title, "Category 5")
        self.assertEqual(context['categories'][5].title, "Category 6")

        templates = response.templates
        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_contact.html')
        self.assertEqual(templates[6].name, 'partial/_credits.html')

        self.assertContains(response, "Check Info")
        self.assertContains(response, "checkinfo@gmail.com")
        self.assertContains(response, "7873923408")
        self.assertContains(response, "facebook.com/checkinfofacebook")
        self.assertContains(response, "instagram.com/checkinfoinstagram")
        self.assertContains(response, "twitter.com/checkinfotwitter")
        self.assertContains(response, "linkedin.com/in/checkinfolinkedin")
        self.assertContains(response, "youtube.com/channel/checkinfoyoutube")
        self.assertContains(response, "pinterest.com/checkinfopinterest")
        self.assertContains(response, "Category 1")
        self.assertContains(response, "Category 2")
        self.assertContains(response, "Category 3")
        self.assertContains(response, "Category 4")
        self.assertContains(response, "Category 5")
        self.assertContains(response, "Category 6")

    def test_colors(self):

        colors()

        client = Client()

        response = client.get('/colors/')
        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, "Colors")
        self.assertEqual(context['color'].navbar, "ff44e7")
        self.assertEqual(context['color'].category, "ff4444")
        self.assertEqual(context['color'].active, "7044ff")
        self.assertEqual(context['color'].footer, "44f8ff")
        self.assertEqual(context['color'].text, "44ffa8")
        self.assertEqual(context['color'].title, "fcff44")
        self.assertEqual(context['color'].title_hover, "d50e04")

        self.assertContains(response, "Colors")
        self.assertContains(response, "background-color: #ff44e7;")
        self.assertContains(response, "background-color: #ff4444;")
        self.assertContains(response, "background-color: #7044ff;")
        self.assertContains(response, "background-color: #44f8ff;")
        self.assertContains(response, "color: #44ffa8;")
        self.assertContains(response, "color: #fcff44;")
        self.assertContains(response, "color: #d50e04;")

    def test_images(self):

        images()

        client = Client()

        response = client.get('/images/')
        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['website'].title, "Images")
        self.assertEqual(context['icon'].shortcut.url, "/media/images/shortcut.png")
        self.assertEqual(context['icon'].account.url, "/media/images/account.png")
        self.assertEqual(context['icon'].cart.url, "/media/images/cart.png")
        self.assertEqual(context['icon'].search.url, "/media/images/search.png")
        self.assertEqual(context['icon'].home.url, "/media/images/home.png")
        self.assertEqual(context['banners'][0].images.url, "/media/images/banner-1.jpg")
        self.assertEqual(context['banners'][1].images.url, "/media/images/banner-2.jpg")

        templates = response.templates
        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_banners.html')

        self.assertContains(response, "Images")
        self.assertContains(response, 'href="/media/images/shortcut.png"')
        self.assertContains(response, 'src="/media/images/account.png"')
        self.assertContains(response, 'src="/media/images/cart.png"')
        self.assertContains(response, 'src="/media/images/search.png"')
        self.assertContains(response, 'src="/media/images/home.png"')
        self.assertContains(response, 'src="/media/images/banner-1.jpg"')
        self.assertContains(response, 'src="/media/images/banner-2.jpg"')


class ShowProductsViewTest(TestCase):

    def test_products_on_home(self):

        products()

        client = Client()

        response = client.get('/products/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        for x in range(4):
            self.assertEqual(context['categories'][x].title, f'Category {x+1}')
            self.assertContains(response, f'Category {x+1}')

        y = 0
        for x in range(2):

            self.assertEqual(context['products'][y].title, f'Category 1 Product {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertContains(response, f'Category 1 Product {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))

            y += 1

            self.assertEqual(context['products'][y].title, f'Category 1 Promotional {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertEqual(context['products'][y].promotional_price, Decimal(f'{x}.{x}'))
            self.assertContains(response, f'Category 1 Promotional {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))
            if x > 0:
                self.assertContains(response, money_format(Decimal(f'{x}.{x}'), 'USD', 'en_US'))

            y += 1

            if y == 8:
                break

            self.assertEqual(context['products'][y].title, f'Category 1 Price type 3 {x + 1}')
            self.assertEqual(context['products'][y].price, None)
            self.assertEqual(context['products'][y].price_type, '3')
            self.assertContains(response, f'Category 1 Price type 3 {x + 1}')

            y += 1

        templates = response.templates
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")

    def test_products_on_home_page_2(self):

        products()

        client = Client()

        response = client.get('/products/?page=2')

        self.assertEqual(response.status_code, 200)

        context = response.context

        for x in range(4):
            self.assertEqual(context['categories'][x].title, f'Category {x+1}')
            self.assertContains(response, f'Category {x+1}')

        y = 0

        self.assertEqual(context['products'][y].title, f'Category 1 Price type 3 3')
        self.assertEqual(context['products'][y].price, None)
        self.assertEqual(context['products'][y].price_type, '3')
        self.assertContains(response, f'Category 1 Price type 3 3')

        y = 1
        for x in [3, 4]:

            self.assertEqual(context['products'][y].title, f'Category 1 Product {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertContains(response, f'Category 1 Product {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))

            y += 1

            self.assertEqual(context['products'][y].title, f'Category 1 Promotional {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertEqual(context['products'][y].promotional_price, Decimal(f'{x}.{x}'))
            self.assertContains(response, f'Category 1 Promotional {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))
            if x > 0:
                self.assertContains(response, money_format(Decimal(f'{x}.{x}'), 'USD', 'en_US'))

            y += 1

            if y == 8:
                break

            self.assertEqual(context['products'][y].title, f'Category 1 Price type 3 {x + 1}')
            self.assertEqual(context['products'][y].price, None)
            self.assertEqual(context['products'][y].price_type, '3')
            self.assertContains(response, f'Category 1 Price type 3 {x + 1}')

            y += 1

        templates = response.templates
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")

    def test_products_by_category(self):

        products()

        client = Client()

        response = client.get('/products/c/category-2/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        for x in range(4):
            self.assertEqual(context['categories'][x].title, f'Category {x+1}')
            self.assertContains(response, f'Category {x+1}')

        y = 0
        for x in range(2):

            self.assertEqual(context['products'][y].title, f'Category 2 Product {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertContains(response, f'Category 2 Product {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))

            y += 1

            self.assertEqual(context['products'][y].title, f'Category 2 Promotional {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertEqual(context['products'][y].promotional_price, Decimal(f'{x}.{x}'))
            self.assertContains(response, f'Category 2 Promotional {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))
            if x > 0:
                self.assertContains(response, money_format(Decimal(f'{x}.{x}'), 'USD', 'en_US'))

            y += 1

            if y == 8:
                break

            self.assertEqual(context['products'][y].title, f'Category 2 Price type 3 {x + 1}')
            self.assertEqual(context['products'][y].price, None)
            self.assertEqual(context['products'][y].price_type, '3')
            self.assertContains(response, f'Category 2 Price type 3 {x + 1}')

            y += 1

        templates = response.templates
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")

    def test_products_by_category_page_2(self):

        products()

        client = Client()

        response = client.get('/products/c/category-2/?page=2')

        self.assertEqual(response.status_code, 200)

        context = response.context

        for x in range(4):
            self.assertEqual(context['categories'][x].title, f'Category {x+1}')
            self.assertContains(response, f'Category {x+1}')

        y = 0

        self.assertEqual(context['products'][y].title, f'Category 2 Price type 3 3')
        self.assertEqual(context['products'][y].price, None)
        self.assertEqual(context['products'][y].price_type, '3')
        self.assertContains(response, f'Category 2 Price type 3 3')

        y = 1
        for x in [3, 4]:

            self.assertEqual(context['products'][y].title, f'Category 2 Product {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertContains(response, f'Category 2 Product {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))

            y += 1

            self.assertEqual(context['products'][y].title, f'Category 2 Promotional {x + 1}')
            self.assertEqual(context['products'][y].price, Decimal(x+1))
            self.assertEqual(context['products'][y].promotional_price, Decimal(f'{x}.{x}'))
            self.assertContains(response, f'Category 2 Promotional {x + 1}')
            self.assertContains(response, money_format(Decimal(x+1), 'USD', 'en_US'))
            if x > 0:
                self.assertContains(response, money_format(Decimal(f'{x}.{x}'), 'USD', 'en_US'))

            y += 1

            if y == 8:
                break

            self.assertEqual(context['products'][y].title, f'Category 2 Price type 3 {x + 1}')
            self.assertEqual(context['products'][y].price, None)
            self.assertEqual(context['products'][y].price_type, '3')
            self.assertContains(response, f'Category 2 Price type 3 {x + 1}')

            y += 1

        templates = response.templates
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")

    def test_category_error_404(self):

        products()

        client = Client()

        response = client.get('/products/c/category-6/')

        self.assertEqual(response.status_code, 404)

    def test_products_by_search(self):

        products()

        client = Client()

        response = client.get('/products/?search=Product+1')

        self.assertEqual(response.status_code, 200)

        context = response.context

        for x in range(4):
            self.assertEqual(context['categories'][x].title, f'Category {x+1}')
            self.assertContains(response, f'Category {x+1}')

        y = 0
        for x in range(2):

            self.assertEqual(context['products'][y].title, f'Category {x + 1} Product 1')
            self.assertEqual(context['products'][y].price, Decimal('1.00'))
            self.assertContains(response, f'Category {x + 1} Product 1')
            self.assertContains(response, money_format(Decimal('1.00'), 'USD', 'en_US'))

            y += 1

        templates = response.templates
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_products.html')
        self.assertEqual(templates[6].name, "partial/_pagination.html")


class ShowProductViewTest(TestCase):

    def test_product_404(self):

        product_type('1')

        client = Client()

        response = client.get('/products/p/product-2/')

        self.assertEqual(response.status_code, 404)

    def test_product_1(self):
        """
        Test product when price type equal 1
        """

        product_type('1')

        client = Client()

        response = client.get('/products/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['product'].title, 'Product')
        self.assertEqual(context['product'].price_type, '1')
        self.assertEqual(context['product'].price, Decimal(30000))

        size = ((1, 1), (0, 1), (0, 10))

        op = 0

        for x in range(3):

            self.assertEqual(context['groups'][x].title, f'group {x + 1}')
            self.assertEqual(context['groups'][x].minimum, size[x][0])
            self.assertEqual(context['groups'][x].maximum, size[x][1])
            self.assertEqual(context['groups'][x].price_type, None)

            for y in range(3):

                self.assertEqual(context['options'][op].title, f'option {y+1}')
                self.assertEqual(context['options'][op].minimum, 0)
                self.assertEqual(context['options'][op].maximum, size[x][1])
                self.assertEqual(context['options'][op].price, None)

                op += 1

            if x > 0:

                self.assertEqual(context['options'][op].title, "Readonly")
                self.assertEqual(context['options'][op].maximum, context['options'][op].minimum)
                self.assertEqual(context['options'][op].minimum, size[x][1])
                self.assertEqual(context['options'][op].price, None)

                op += 1

        templates = response.templates
        self.assertEqual(templates[0].name, 'website.html')
        self.assertEqual(templates[1].name, 'base.html')
        self.assertEqual(templates[2].name, 'partial/_head.html')
        self.assertEqual(templates[3].name, 'partial/_top_navbar.html')
        self.assertEqual(templates[4].name, 'partial/_categories.html')
        self.assertEqual(templates[5].name, 'partial/_product.html')
        self.assertEqual(templates[6].name, "partial/_credits.html")

    def test_product_2(self):
        """
        Test product when price type equal 2
        """

        product_type('2')

        client = Client()

        response = client.get('/products/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['product'].title, 'Product')
        self.assertEqual(context['product'].price_type, '2')
        self.assertEqual(context['product'].price, Decimal(30000))

        size = ((1, 1), (0, 1), (0, 10))

        op = 0

        for x in range(3):

            self.assertEqual(context['groups'][x].title, f'group {x + 1}')
            self.assertEqual(context['groups'][x].minimum, size[x][0])
            self.assertEqual(context['groups'][x].maximum, size[x][1])
            self.assertEqual(context['groups'][x].price_type, '1')

            for y in range(3):
                self.assertEqual(context['options'][op].title, f'option {y+1}')
                self.assertEqual(context['options'][op].minimum, 0)
                self.assertEqual(context['options'][op].maximum, size[x][1])
                self.assertEqual(context['options'][op].price, 200)

                op += 1

            if x > 0:
                self.assertEqual(context['options'][op].title, "Readonly")
                self.assertEqual(context['options'][op].maximum, context['options'][op].minimum)
                self.assertEqual(context['options'][op].minimum, size[x][1])
                self.assertEqual(context['options'][op].price, 200)

                op += 1

    def test_product_3(self):
        """
        Test product when price type equal 3
        """

        product_type('3')

        client = Client()

        response = client.get('/products/p/product/')

        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(context['product'].title, 'Product')
        self.assertEqual(context['product'].price_type, '3')
        self.assertEqual(context['product'].price, None)

        size = ((1, 1), (0, 1), (0, 10))

        op = 0

        for x in range(3):

            self.assertEqual(context['groups'][x].title, f'group {x + 1}')
            self.assertEqual(context['groups'][x].minimum, size[x][0])
            self.assertEqual(context['groups'][x].maximum, size[x][1])
            self.assertEqual(context['groups'][x].price_type, '1')

            for y in range(3):
                self.assertEqual(context['options'][op].title, f'option {y+1}')
                self.assertEqual(context['options'][op].minimum, 0)
                self.assertEqual(context['options'][op].maximum, size[x][1])
                self.assertEqual(context['options'][op].price, 200)

                op += 1

            if x > 0:
                self.assertEqual(context['options'][op].title, "Readonly")
                self.assertEqual(context['options'][op].maximum, context['options'][op].minimum)
                self.assertEqual(context['options'][op].minimum, size[x][1])
                self.assertEqual(context['options'][op].price, 200)

                op += 1

