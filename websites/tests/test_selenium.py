from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .scenarios import check_info, colors, images, products, product_type
from websites.models import Websites
from websites.utils.utils import money_format
from decimal import Decimal


class WebsiteTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = WebDriver('websites/tests/Webdriver/chromedriver')
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_website(self):

        check_info()

        self.selenium.get('%s%s' % (self.live_server_url, '/checkinfo/'))

        element = self.selenium.find_element_by_id('home_category')
        self.assertEqual(element.text, "Highlight")

        for x in range(6):
            element = self.selenium.find_element_by_id(f'category-{x+1}')
            self.assertEqual(element.text, f'Category {x+1}')

        element = self.selenium.find_element_by_id('top_navbar')
        self.assertEqual(element.text, f'Check Info\n0')

        contacts = (
            ('instagram', 'https://www.instagram.com/checkinfoinstagram'),
            ('facebook', 'https://www.facebook.com/checkinfofacebook'),
            ('twitter', 'https://www.twitter.com/checkinfotwitter'),
            ('linkedin', 'https://www.linkedin.com/in/checkinfolinkedin'),
            ('pinterest', 'https://www.pinterest.com/checkinfopinterest'),
            ('youtube', 'https://www.youtube.com/channel/checkinfoyoutube'),
        )

        for contact in contacts:

            element = self.selenium.find_element_by_id(contact[0])
            self.assertEqual(element.get_attribute("href"), contact[1])

        contacts = (
            ('telephone', 'Tel:\n7873923408'),
            ('email', 'Email:\ncheckinfo@gmail.com'),
            ('whatsapp', '(78) 73923408'),
        )

        for contact in contacts:
            element = self.selenium.find_element_by_id(contact[0])
            self.assertEqual(element.text, contact[1])

        colors()

        self.selenium.get('%s%s' % (self.live_server_url, '/colors/'))

        # TODO: Improve this code

        colors_ = (
            ('navbar', 'rgba(255, 68, 231, 1)'),
            ('category', 'rgba(255, 68, 68, 1)'),
            ('active', 'rgba(112, 68, 255, 1)'),
            ('footer', 'rgba(68, 248, 255, 1)'),
        )

        for color in colors_:
            element = self.selenium.find_element_by_class_name(color[0])
            self.assertEqual(element.value_of_css_property("background-color"), color[1])


class ShowProductsTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = WebDriver('websites/tests/Webdriver/chromedriver')
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def check_categories(self):
        """
            Check categories elements' information
        """

        element = self.selenium.find_element_by_id('home_category')
        self.assertEqual(element.text, "Highlight")

        for x in range(4):
            element = self.selenium.find_element_by_id(f'category-{x + 1}')
            self.assertEqual(element.text, f'Category {x + 1}')

    def check_products(self, category):

        y = 0
        for x in range(2):

            text = f'Category {category} Product {x + 1}\n{money_format(x+1, "USD", "en_US")}'

            element = self.selenium.find_element_by_id(f'category-{category}-product-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

            text = f'Category {category} Promotional {x + 1}\n{money_format(x+1, "USD", "en_US")}'
            text += f' {money_format(Decimal(f"{x}.{x}"), "USD", "en_US")}' if x > 0 else ''

            element = self.selenium.find_element_by_id(f'category-{category}-promotional-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

            if y == 8:
                break

            text = f'Category {category} Price type 3 {x + 1}'

            element = self.selenium.find_element_by_id(f'category-{category}-price-type-3-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

    def check_products_2(self, category):

        text = f'Category {category} Price type 3 3'

        element = self.selenium.find_element_by_id(f'category-{category}-price-type-3-3')
        self.assertEqual(element.text, text)

        y = 1
        for x in [3, 4]:

            text = f'Category {category} Product {x + 1}\n{money_format(x + 1, "USD", "en_US")}'

            element = self.selenium.find_element_by_id(f'category-{category}-product-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

            text = f'Category {category} Promotional {x + 1}\n{money_format(x + 1, "USD", "en_US")}'
            text += f' {money_format(Decimal(f"{x}.{x}"), "USD", "en_US")}' if x > 0 else ''

            element = self.selenium.find_element_by_id(f'category-{category}-promotional-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

            if y == 8:
                break

            text = f'Category {category} Price type 3 {x + 1}'

            element = self.selenium.find_element_by_id(f'category-{category}-price-type-3-{x + 1}')
            self.assertEqual(element.text, text)

            y += 1

    def test_products(self):

        products()

        self.selenium.get('%s%s' % (self.live_server_url, '/products/'))

        self.check_categories()
        self.check_products(1)

        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')
        next_page = self.selenium.find_element_by_id('next_page')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(next_page.text, '»')

        actions = ActionChains(self.selenium)
        actions.click(page2)
        actions.perform()

        self.check_categories()
        self.check_products_2(1)

        previous_page = self.selenium.find_element_by_id('previous_page')
        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(previous_page.text, '«')

        category_2 = self.selenium.find_element_by_id('category-2')

        actions = ActionChains(self.selenium)
        actions.click(category_2)
        actions.perform()


        self.check_categories()

        self.check_products(2)

        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')
        next_page = self.selenium.find_element_by_id('next_page')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(next_page.text, '»')

        actions = ActionChains(self.selenium)
        actions.click(page2)
        actions.perform()

        self.check_categories()
        self.check_products_2(2)

        previous_page = self.selenium.find_element_by_id('previous_page')
        page1 = self.selenium.find_element_by_id('page1')
        page2 = self.selenium.find_element_by_id('page2')

        self.assertEqual(page1.text, '1')
        self.assertEqual(page2.text, '2')
        self.assertEqual(previous_page.text, '«')

        search = self.selenium.find_element_by_id('search')

        actions = ActionChains(self.selenium)
        actions.click(search)
        actions.send_keys("Product 1")
        actions.key_down(Keys.ENTER)
        actions.perform()

        for x in range(2):

            text = f'Category {x + 1} Product 1\n{money_format(1, "USD", "en_US")}'

            element = self.selenium.find_element_by_id(f'category-{x + 1}-product-1')
            self.assertEqual(element.text, text)


class ShowProductTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = WebDriver('websites/tests/Webdriver/chromedriver')
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def check_product(self):

        element = self.selenium.find_element_by_id('product_image').find_element_by_tag_name('img')
        self.assertEqual(element.get_attribute("src"), f'{self.live_server_url}/static/media/category.png')

        element = self.selenium.find_element_by_id('product_title')
        self.assertEqual(element.text, f'Product')

    def check_groups(self, price_type):

        for x in range(3):

            element = self.selenium.find_element_by_id(f'group{x + 1}')
            self.assertEqual(element.text, f'group {x + 1}')

            if price_type != '1':
                text = '$200.00\n$200.00\n$200.00'
                if x > 0:
                    text += '\n$200.00'
            else:
                text = 'option 1\noption 2\noption 3'
                if x > 0:
                    text += '\nReadonly'

            element = self.selenium.find_element_by_id(f'group{x + 1}_options')
            self.assertEqual(element.text, text)

    def interact_with_options(self, options):

        group = 1
        aux = 1

        for option in options:

            if (aux == 4 and group == 1) or aux == 5:
                group += 1
                aux = 1

            element = self.selenium.find_element_by_id(f'{option}')

            actions = ActionChains(self.selenium)
            actions.click(element)

            if element.get_attribute('type') == 'number':
                actions.send_keys('2')

            actions.perform()

            element = self.selenium.find_element_by_id(f'group{group}_title')

            if aux == 4:
                self.assertEqual(element.text, f'Readonly')
            else:
                self.assertEqual(element.text, f'option {aux}')

            aux += 1

    def test_product_1(self):

        price_type = '1'

        product_type(price_type)

        self.selenium.get('%s%s' % (self.live_server_url, '/products/'))

        element = self.selenium.find_element_by_id(f'product')

        actions = ActionChains(self.selenium)
        actions.click(element)
        actions.perform()

        self.check_product()
        self.check_groups(price_type)

        total = '$30,000.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)

        self.interact_with_options(range(12)[1:])

        total = '$30,000.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)

    def test_product_2(self):

        price_type = '2'

        product_type(price_type)

        self.selenium.get('%s%s' % (self.live_server_url, '/products/'))

        element = self.selenium.find_element_by_id(f'product')

        actions = ActionChains(self.selenium)
        actions.click(element)
        actions.perform()

        self.check_product()
        self.check_groups(price_type)

        total = '$32,200.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)

        self.interact_with_options(range(23)[12:])

        total = '$34,200.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)

    def test_product_3(self):

        price_type = '3'

        product_type(price_type)

        self.selenium.get('%s%s' % (self.live_server_url, '/products/'))

        element = self.selenium.find_element_by_id(f'product')

        actions = ActionChains(self.selenium)
        actions.click(element)
        actions.perform()

        self.check_product()
        self.check_groups(price_type)

        total = '$2,200.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)

        self.interact_with_options(range(34)[23:])

        total = '$4,200.00'

        element = self.selenium.find_element_by_id('product_total')
        self.assertEqual(element.text, total)
