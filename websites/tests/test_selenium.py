from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .scenarios import create_scenario_1, create_scenario_2
from websites.models import Products, Groups, Options
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

    def check_contact(self, website, contact):
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
        self.check_contact(self.website, self.contact)

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
        self.check_contact(self.website, self.contact)

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
        self.check_contact(self.website, self.contact)

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
        self.check_contact(self.website, self.contact)

        previous_page = self.selenium.find_element_by_id('previous_page')
        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(previous_page.text, '«')

        search = self.selenium.find_element_by_id('search')

        actions = ActionChains(self.selenium)
        actions.click(search)
        actions.send_keys("one")
        actions.key_down(Keys.ENTER)
        actions.perform()

        products = Products.objects.filter(websites=self.website, is_available=True,
                                           title__icontains='one').order_by('position')
        products = Paginator(products, 8)
        products = products.get_page(1)

        self.check_categories(self.categories)
        self.check_products(products)
        self.check_contact(self.website, self.contact)


class ShowProductViewTestSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website, cls.categories = create_scenario_2()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def check_product(self, product):
        element = self.selenium.find_element_by_id('product_image').find_element_by_tag_name('img')
        self.assertEqual(element.get_attribute("src"), f'{self.live_server_url}/static/media/category.png')

        element = self.selenium.find_element_by_id('product_title')
        self.assertEqual(element.text, product.title)

        element = self.selenium.find_element_by_id('product_description')
        self.assertEqual(element.text, product.description)

    def check_groups(self, groups):

        for group in groups:

            element_id = str(group).replace('-', '')

            element = self.selenium.find_element_by_id(f'{element_id}')
            self.assertEqual(element.text, group.title)

            if group.price_type:
                text = '$200.00\n$200.00\n$200.00\n$200.00'
            else:
                text = 'Op1\nOp2\nOp3\nReadonly'

            element = self.selenium.find_element_by_id(f'{element_id}_options')
            self.assertEqual(element.text, text)

    def interact_with_options(self, groups):

        for group in groups:

            options = Options.objects.filter(groups=group).order_by('position')
            element_id = str(group).replace('-', '')

            for option in options:

                element = self.selenium.find_element_by_id(f'{option.pk}')

                actions = ActionChains(self.selenium)
                actions.click(element)

                if element.get_attribute('type') == 'number':
                    actions.send_keys('2')

                actions.perform()

                if option.minimum != option.maximum and option.maximum > 1:
                    element = self.selenium.find_element_by_id(f'{element_id}_title')
                    self.assertEqual(element.text, option.title)

    def test_interactive(self):

        products = Products.objects.filter(websites=self.website).order_by('position')

        for product in products:

            self.selenium.get('%s%s' % (self.live_server_url, f'/{self.website.url}/'))

            groups = Groups.objects.filter(products=product).order_by('position')

            element = self.selenium.find_element_by_id(product.slug)

            actions = ActionChains(self.selenium)
            actions.click(element)
            actions.perform()

            self.check_product(product)
            self.check_groups(groups)

            if product.price_type == '1':
                total = '$30,000.00'
            elif product.price_type == '2':
                total = '$31,400.00'
            else:
                total = '$1,400.00'

            element = self.selenium.find_element_by_id('product_total')
            self.assertEqual(element.text, total)

            self.interact_with_options(groups)

            if product.price_type == '2':
                total = '$33,400.00'
            elif product.price_type == '3':
                total = '$3,400.00'

            element = self.selenium.find_element_by_id('product_total')
            self.assertEqual(element.text, total)
