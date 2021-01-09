from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from .scenarios import create_scenario_1
from websites.models import Products
from django.core.paginator import Paginator


class ShowProductsViewTestSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website, cls.contact, cls.categories = create_scenario_1()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def check_others(self, website, contact):
        """
            Check top navbar and contact elements' information
        """

        element = self.selenium.find_element_by_id('top_navbar')
        self.assertEqual(element.text, f'{website.title}\n0')

        element = self.selenium.find_element_by_id('instagram')
        self.assertEqual(element.get_attribute("href"), f'https://www.instagram.com/{contact.instagram}')

        element = self.selenium.find_element_by_id('facebook')
        self.assertEqual(element.get_attribute("href"), f'https://www.facebook.com/{contact.facebook}')

        element = self.selenium.find_element_by_id('twitter')
        self.assertEqual(element.get_attribute("href"), f'https://www.twitter.com/{contact.twitter}')

        element = self.selenium.find_element_by_id('linkedin')
        self.assertEqual(element.get_attribute("href"), f'https://www.linkedin.com/in/{contact.linkedin}')

        element = self.selenium.find_element_by_id('telephone')
        self.assertEqual(element.text, f'Tel:\n{contact.telephone}')

        element = self.selenium.find_element_by_id('email')
        self.assertEqual(element.text, f'Email:\n{contact.email}')

        element = self.selenium.find_element_by_id('whatsapp')
        self.assertEqual(element.text, f'(78) 73923408')

    def check_categories(self, categories):
        """
            Check categories elements' information
        """

        element = self.selenium.find_element_by_id('home_category')
        self.assertEqual(element.text, "Highlight")

        for category in categories:
            element = self.selenium.find_element_by_id(category.slug)
            self.assertEqual(element.text, category.title)

    def check_products(self, products):

        for product in products:

            text = f'{product.title}\n'

            if product.price:
                text += f'{product.get_price()}'

            if product.promotional_price:
                text += f' {product.get_promotional_price()}'

            element = self.selenium.find_element_by_id(product.slug)
            self.assertEqual(element.text, text)

    def test_interactive(self):
        """
            Check if the information registered in the database is visible on the HTML page. Products is a Paginator
            object.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/website/'))

        products = Products.objects.filter(websites=self.website, is_available=True, show_on_home=True
                                           ).order_by('position')
        products = Paginator(products, 8)

        products = products.get_page(1)

        self.check_categories(self.categories)
        self.check_products(products)
        self.check_others(self.website, self.contact)

        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')
        next_page = self.selenium.find_element_by_id('next_page')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(next_page.text, '»')

        actions = ActionChains(self.selenium)
        actions.click(page2)
        actions.perform()

        products = Products.objects.filter(websites=self.website, is_available=True, show_on_home=True
                                           ).order_by('position')
        products = Paginator(products, 8)
        products = products.get_page(2)

        self.check_categories(self.categories)
        self.check_products(products)
        self.check_others(self.website, self.contact)

        previous_page = self.selenium.find_element_by_id('previous_page')
        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(previous_page.text, '«')

        category_2 = self.selenium.find_element_by_id(self.categories[1].slug)

        actions = ActionChains(self.selenium)
        actions.click(category_2)
        actions.perform()

        products = Products.objects.filter(categories=self.categories[1], is_available=True).order_by('position')
        products = Paginator(products, 8)

        products = products.get_page(1)

        self.check_categories(self.categories)
        self.check_products(products)
        self.check_others(self.website, self.contact)

        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')
        next_page = self.selenium.find_element_by_id('next_page')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(next_page.text, '»')

        actions = ActionChains(self.selenium)
        actions.click(page2)
        actions.perform()

        products = Products.objects.filter(categories=self.categories[1], is_available=True).order_by('position')
        products = Paginator(products, 8)
        products = products.get_page(2)

        self.check_categories(self.categories)
        self.check_products(products)
        self.check_others(self.website, self.contact)

        previous_page = self.selenium.find_element_by_id('previous_page')
        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(previous_page.text, '«')
