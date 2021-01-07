from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from websites.utils.utils import money_format
from ..models import Websites, Contacts, Categories, Products, Groups, Options
from decimal import *
from django.utils.text import slugify


class ShowProductsViewTestSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website = Websites.objects.create(url='website', title="Website")
        cls.c1 = Categories.objects.create(websites=cls.website, title="Category 1", position=1)
        cls.c2 = Categories.objects.create(websites=cls.website, title="Category 2", position=2)
        cls.c3 = Categories.objects.create(websites=cls.website, title="Category 3", position=4)
        cls.c4 = Categories.objects.create(websites=cls.website, title="Category 4", position=3)

        Contacts.objects.create(websites=cls.website, telephone='7873923408', email='example@email.com',
                                facebook='example', instagram='example', twitter='example', linkedin='example',
                                whatsapp='7873923408')

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

        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(60)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_check_elements(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/website/'))

        # Find elements
        top_navbar = self.selenium.find_element_by_id("top_navbar")
        home = self.selenium.find_element_by_id("home_category")
        c1 = self.selenium.find_element_by_id(self.c1.slug)
        c2 = self.selenium.find_element_by_id(self.c2.slug)
        c3 = self.selenium.find_element_by_id(self.c3.slug)
        c4 = self.selenium.find_element_by_id(self.c4.slug)

        # Check elements
        self.assertEqual(top_navbar.text, "Website\n0")
        self.assertEqual(home.text, "Highlight")
        self.assertEqual(c1.text, "Category 1")
        self.assertEqual(c2.text, "Category 2")
        self.assertEqual(c3.text, "Category 3")
        self.assertEqual(c4.text, "Category 4")

        products = []

        for product in self.products:
            element_id = slugify(product[0])
            products.append(self.selenium.find_element_by_id(element_id))

        for x, product in enumerate(products):
            money = money_format(self.products[x][1], self.website.currency, self.website.language)
            self.assertEqual(product.text, f'{self.products[x][0]}\n{money}')

        instagram = self.selenium.find_element_by_id("instagram")
        facebook = self.selenium.find_element_by_id("facebook")
        twitter = self.selenium.find_element_by_id("twitter")
        linkedin = self.selenium.find_element_by_id("linkedin")

        telephone = self.selenium.find_element_by_id("telephone")
        email = self.selenium.find_element_by_id("email")

        whatsapp = self.selenium.find_element_by_id("whatsapp")

        self.assertEqual(instagram.get_attribute("href"), "https://www.instagram.com/example")
        self.assertEqual(facebook.get_attribute("href"), "https://www.facebook.com/example")
        self.assertEqual(twitter.get_attribute("href"), "https://www.twitter.com/example")
        self.assertEqual(linkedin.get_attribute("href"), "https://www.linkedin.com/in/example")

        self.assertEqual(telephone.text, "Tel:\n7873923408")
        self.assertEqual(email.text, "Email:\nexample@email.com")
        self.assertEqual(whatsapp.text, "(78) 73923408")

        page1 = self.selenium.find_element_by_id("page1")
        page2 = self.selenium.find_element_by_id("page2")
        next_page = self.selenium.find_element_by_id("next_page")

        self.assertEqual(page1.text, "1")
        self.assertEqual(page2.text, "2")
        self.assertEqual(next_page.text, "»")
