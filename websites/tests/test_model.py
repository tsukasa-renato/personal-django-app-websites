from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Websites, Colors, Icons, Banners, Categories, Products, Groups, Options


class WebsiteTests(TestCase):
    """
    Test the following models: websites, colors, icons, banners, contacts
    """

    def test_colors(self):

        # Valid values
        values = ('a', 'A', 'f', 'F', '0', '9', 'ab', 'AB', '01', '98', 'AbFe', '0AbDe2', 'fff555')
        compare = ('00000a', '00000a', '00000f', '00000f', '000000', '000009', '0000ab', '0000ab',
                   '000001', '000098', '00abfe', '0abde2', 'fff555')

        for x, v in enumerate(values):
            website = Websites.objects.create(url=v, title="title")
            color = Colors.objects.create(websites=website, navbar=v, category=v, active=v, footer=v, text=v,
                                          title=v, title_hover=v)
            self.assertEqual(color.navbar, compare[x])
            self.assertEqual(color.category, compare[x])
            self.assertEqual(color.active, compare[x])
            self.assertEqual(color.footer, compare[x])
            self.assertEqual(color.text, compare[x])
            self.assertEqual(color.title, compare[x])
            self.assertEqual(color.title_hover, compare[x])

        # Invalid values
        with self.assertRaisesMessage(ValidationError, "Navbar error: invalid hexadecimal"):
            Colors.objects.create(websites=website, navbar='Z')

        with self.assertRaisesMessage(ValidationError, "Category error: invalid hexadecimal"):
            Colors.objects.create(websites=website, category='Z')

        with self.assertRaisesMessage(ValidationError, "Active error: invalid hexadecimal"):
            Colors.objects.create(websites=website, active='Z')

        with self.assertRaisesMessage(ValidationError, "Footer error: invalid hexadecimal"):
            Colors.objects.create(websites=website, footer='Z')

        with self.assertRaisesMessage(ValidationError, "Text error: invalid hexadecimal"):
            Colors.objects.create(websites=website, text='Z')

        with self.assertRaisesMessage(ValidationError, "Title error: invalid hexadecimal"):
            Colors.objects.create(websites=website, title='Z')

        with self.assertRaisesMessage(ValidationError, "Title hover error: invalid hexadecimal"):
            Colors.objects.create(websites=website, title_hover='Z')

    # You need to download the images from the internet
    def test_images(self):

        # Create folder in websites/tests/ and you download images from the internet

        website = Websites.objects.create(url='images', title="Images")
        icon = Icons.objects.create(websites=website, shortcut='images/shortcut.png', account='images/account.png',
                                    cart='images/cart.png', search='images/search.png', home='images/home.png')

        self.assertEqual(icon.shortcut.url, '/media/images/shortcut.png')
        self.assertEqual(icon.account.url, '/media/images/account.png')
        self.assertEqual(icon.cart.url, '/media/images/cart.png')
        self.assertEqual(icon.search.url, '/media/images/search.png')
        self.assertEqual(icon.home.url, '/media/images/home.png')

        banner = Banners.objects.create(websites=website, images='images/banner-1.jpg')
        self.assertEqual(banner.images.url, '/media/images/banner-1.jpg')

        banner = Banners.objects.create(websites=website, images='images/banner-2.jpg')
        self.assertEqual(banner.images.url, '/media/images/banner-2.jpg')


class InitialDataTest(TestCase):
    """
    Register necessary initial data for the tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.website = Websites.objects.create(url='url', title="_title")
        cls.category = Categories.objects.create(websites=cls.website, title="_title")
        cls.product = Products.objects.create(websites=cls.website, categories=cls.category, title="_title", price=1)
        cls.group = Groups.objects.create(websites=cls.website, products=cls.product, title="_title")
        cls.option = Options.objects.create(websites=cls.website, groups=cls.group, title="_title")


class ProductsModelTest(InitialDataTest):

    def test_unique_constraints(self):
        """
        Register two products with same website and title (slug)
        """

        with self.assertRaises(Exception):
            Products.objects.create(websites=self.website, categories=self.category, title="_title", price=1)

    def test_check_price_type_invalid_values(self):
        """
        Register products using invalid values for price type
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Price type needs be string - type received: " + str(type(None))):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type=None)

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> '1' '2' '3'"):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type='Letters')

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> '1' '2' '3'"):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type='*')

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> '1' '2' '3'"):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type='4')

        with self.assertRaisesMessage(ValidationError,
                                      "Price type needs be string - type received: " + str(type(1))):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type=1)

        with self.assertRaisesMessage(ValidationError,
                                      "Price type needs be string - type received: " + str(type(1.1))):
            Products.objects.create(websites=self.website, categories=self.category, title="title",
                                    price_type=1.1)

    def test_check_price_type_valid_values(self):
        """
        Register products using valid values for price type
        """

        Products.objects.create(websites=self.website, categories=self.category, title="price type = 1",
                                price=1, price_type='1')
        Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                price=1, price_type='2')
        Products.objects.create(websites=self.website, categories=self.category, title="price type = 3",
                                price_type='3')

        self.assertQuerysetEqual(Products.objects.all().order_by('pk'),
                                 ['<Products: _title>', '<Products: price-type-1>', '<Products: price-type-2>',
                                  '<Products: price-type-3>'])

    def test_price_type_requires_a_price(self):
        """
        Register products with price type 1 and 2 and without price
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Price type = 1 requires a price. Enter a price or change the type price"):
            Products.objects.create(websites=self.website, categories=self.category, title="price type = 1",
                                    price_type='1')

        with self.assertRaisesMessage(ValidationError,
                                      "Price type = 2 requires a price. Enter a price or change the type price"):
            Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                    price_type='2')

    def test_price_type_dont_requires_a_price(self):
        """
        Register products with price type 3 and with price
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Price type = 3 don't requires a price. Remove the price or change the type price"
                                      ):
            Products.objects.create(websites=self.website, categories=self.category, title="price type = 3",
                                    price=1, price_type='3')

    def test_get_real_price(self):
        """
        Register a product with price, other with price and promotional price, and other without price and call get
        real price function
        """

        product = Products.objects.create(websites=self.website, categories=self.category, title="price",
                                          price=2, price_type='1')
        self.assertEqual(product.get_real_price(), 2)

        product = Products.objects.create(websites=self.website, categories=self.category, title="promotional price",
                                          price=2, promotional_price=1, price_type='1')
        self.assertEqual(product.get_real_price(), 1)

        product = Products.objects.create(websites=self.website, categories=self.category, title="none price",
                                          price_type='3')
        self.assertEqual(product.get_real_price(), None)

    def test_check_price(self):
        """
        Test check price function
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Price needs be positive integer or float - type received: " + str(type('1'))
                                      ):
            Products.objects.create(websites=self.website, categories=self.category, title="price", price='1')

        with self.assertRaisesMessage(ValidationError,
                                      "Promotional price needs be positive integer or float - type received: " +
                                      str(type('1'))
                                      ):
            Products.objects.create(websites=self.website, categories=self.category, title="price", price=2,
                                    promotional_price='1')

        with self.assertRaisesMessage(ValidationError, "Price can't be negative"):
            Products.objects.create(websites=self.website, categories=self.category, title="price", price=-0.1)

        with self.assertRaisesMessage(ValidationError, "Promotional price can't be negative"):
            Products.objects.create(websites=self.website, categories=self.category, title="price", price=2,
                                    promotional_price=-0.1)

        with self.assertRaisesMessage(ValidationError, "Price can't be None when the promotional_price is set"):
            Products.objects.create(websites=self.website, categories=self.category, title="price",
                                    promotional_price=1)

        with self.assertRaisesMessage(ValidationError, "Promotional price can't be greater than price"):
            Products.objects.create(websites=self.website, categories=self.category, title="price", price=1,
                                    promotional_price=2)


class GroupsModelTest(InitialDataTest):

    def test_unique_constraints(self):
        """
        Register two products with same website and title (slug)
        """

        with self.assertRaises(Exception):
            Groups.objects.create(websites=self.website, products=self.product, title="_title")

    def test_check_price_type_invalid_values(self):
        """
        Register groups using invalid values for price type
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> None '1' '2'"):
            Groups.objects.create(websites=self.website, products=self.product, title="title",
                                  price_type='Letters')

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> None '1' '2'"):
            Groups.objects.create(websites=self.website, products=self.product, title="title",
                                  price_type='*')

        with self.assertRaisesMessage(ValidationError,
                                      "Invalid value - type a valid value -> None '1' '2'"):
            Groups.objects.create(websites=self.website, products=self.product, title="title",
                                  price_type='3')

        with self.assertRaisesMessage(ValidationError,
                                      "Price type needs be string or None - type received: " + str(type(1))):
            Groups.objects.create(websites=self.website, products=self.product, title="title",
                                  price_type=1)

        with self.assertRaisesMessage(ValidationError,
                                      "Price type needs be string or None - type received: " + str(type(1.1))):
            Groups.objects.create(websites=self.website, products=self.product, title="title",
                                  price_type=1.1)

    def test_check_price_type_valid_values(self):
        """
        Register products using valid values for price type
        """

        Groups.objects.create(websites=self.website, products=self.product, title="price type = None",
                              price_type=None)

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                          price=1, price_type='2')

        Groups.objects.create(websites=self.website, products=product, title="price type = 1",
                              price_type='1')
        Groups.objects.create(websites=self.website, products=product, title="price type = 2",
                              price_type='2')

        self.assertQuerysetEqual(Groups.objects.all().order_by('pk'),
                                 ['<Groups: _title>', '<Groups: price-type-none>', '<Groups: price-type-1>',
                                  '<Groups: price-type-2>'])

    def test_only_product_price_is_used_set_price_type_to_none(self):
        """
        Register groups with price type 1 and 2 when Product's price type is 1
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Only product price is used, set price type to None"):
            Groups.objects.create(websites=self.website, products=self.product, title="price type = 1",
                                  price_type='1')

        with self.assertRaisesMessage(ValidationError,
                                      "Only product price is used, set price type to None"):
            Groups.objects.create(websites=self.website, products=self.product, title="price type = 2",
                                  price_type='2')

    def test_product_requires_options_price_price_type_cant_be_none(self):
        """
        Register a group with price type None when Product's price type is 2 and 3
        """

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                          price=1, price_type='2')

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires the options price - price type can't be None"):
            Groups.objects.create(websites=self.website, products=product, title="price type = None",
                                  price_type=None)

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires the options price - price type can't be None"):
            Groups.objects.create(websites=self.website, products=product, title="price type = None",
                                  price_type=None)

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 3",
                                          price_type='3')

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires the options price - price type can't be None"):
            Groups.objects.create(websites=self.website, products=product, title="price type = None",
                                  price_type=None)

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires the options price - price type can't be None"):
            Groups.objects.create(websites=self.website, products=product, title="price type = None",
                                  price_type=None)

    def test_check_min_max(self):
        """
        Test check min max function
        """

        with self.assertRaisesMessage(ValidationError, "Minimum needs be positive integer - type received: " +
                                      str(type('1'))):
            Groups.objects.create(websites=self.website, products=self.product, title="title", minimum='1')

        with self.assertRaisesMessage(ValidationError, "Minimum needs be positive integer - type received: " +
                                      str(type(1.1))):
            Groups.objects.create(websites=self.website, products=self.product, title="title", minimum=1.1)

        with self.assertRaisesMessage(ValidationError, "Maximum needs be positive integer - type received: " +
                                      str(type('1'))):
            Groups.objects.create(websites=self.website, products=self.product, title="title", maximum='1')

        with self.assertRaisesMessage(ValidationError, "Maximum needs be positive integer - type received: " +
                                      str(type(1.1))):
            Groups.objects.create(websites=self.website, products=self.product, title="title", maximum=1.1)

        with self.assertRaisesMessage(ValidationError, "Minimum can't be negative"):
            Groups.objects.create(websites=self.website, products=self.product, title="title", minimum=-1)

        with self.assertRaisesMessage(ValidationError, "Maximum can't be negative or zero"):
            Groups.objects.create(websites=self.website, products=self.product, title="title", maximum=-1)

        with self.assertRaisesMessage(ValidationError, "Maximum can't be negative or zero"):
            Groups.objects.create(websites=self.website, products=self.product, title="title", maximum=0)

        with self.assertRaisesMessage(ValidationError, "Minimum can't be greater than the maximum"):
            Groups.objects.create(websites=self.website, products=self.product, title="title", minimum=2, maximum=1)


class OptionsModelTest(InitialDataTest):

    def test_unique_constraints(self):
        """
        Register two products with same website and title (slug)
        """

        with self.assertRaises(Exception):
            Options.objects.create(websites=self.website, groups=self.group, title="_title")

    def test_check_price_type(self):
        """
        Test check price type function of the option
        """

        with self.assertRaisesMessage(ValidationError,
                                      "Only the product price will be used"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", price=1)

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                          price=1, price_type='2')

        group = Groups.objects.create(websites=self.website, products=product, title="price type = 1",
                                      price_type='1')

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires price will be used"):
            Options.objects.create(websites=self.website, groups=group, title="title")

        group = Groups.objects.create(websites=self.website, products=product, title="price type = 2",
                                      price_type='2')

        with self.assertRaisesMessage(ValidationError,
                                      "Product requires price will be used"):
            Options.objects.create(websites=self.website, groups=group, title="title")

    def test_get_real_price(self):
        """
        Register a product with price, other with price and promotional price, and other without price and call get
        real price function
        """

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                          price=1, price_type='2')

        group = Groups.objects.create(websites=self.website, products=product, title="price type = 1",
                                      price_type='1')

        option = Options.objects.create(websites=self.website, groups=group, title="Price", price=2)
        self.assertEqual(option.get_real_price(), 2)

        option = Options.objects.create(websites=self.website, groups=group, title="Promotional price", price=2,
                                        promotional_price=1)
        self.assertEqual(option.get_real_price(), 1)

        option = Options.objects.create(websites=self.website, groups=self.group, title="None price")
        self.assertEqual(option.get_real_price(), None)

    def test_check_price(self):
        """
        Test check price function
        """

        product = Products.objects.create(websites=self.website, categories=self.category, title="price type = 2",
                                          price=1, price_type='2')

        group = Groups.objects.create(websites=self.website, products=product, title="price type = 1",
                                      price_type='1')

        with self.assertRaisesMessage(ValidationError,
                                      "Price needs be positive integer or float - type received: " + str(type('1'))
                                      ):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price", price='2')

        with self.assertRaisesMessage(ValidationError,
                                      "Promotional price needs be positive integer or float - type received: " +
                                      str(type('1'))
                                      ):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price", price=2,
                                   promotional_price='1')

        with self.assertRaisesMessage(ValidationError, "Price can't be negative"):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price", price=-0.1)

        with self.assertRaisesMessage(ValidationError, "Promotional price can't be negative"):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price", price=2,
                                   promotional_price=-0.1)

        with self.assertRaisesMessage(ValidationError, "Price can't be None when the promotional_price is set"):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price",
                                   promotional_price=1)

        with self.assertRaisesMessage(ValidationError, "Promotional price can't be greater than price"):
            Options.objects.create(websites=self.website, groups=group, title="Promotional price", price=1,
                                   promotional_price=2)

    def test_check_min_max(self):
        """
        Test check min max function
        """

        with self.assertRaisesMessage(ValidationError, "Minimum needs be positive integer - type received: " +
                                      str(type('1'))):
            Options.objects.create(websites=self.website, groups=self.group, title="title", minimum='1')

        with self.assertRaisesMessage(ValidationError, "Minimum needs be positive integer - type received: " +
                                      str(type(1.1))):
            Options.objects.create(websites=self.website, groups=self.group, title="title", minimum=1.1)

        with self.assertRaisesMessage(ValidationError, "Maximum needs be positive integer - type received: " +
                                      str(type('1'))):
            Options.objects.create(websites=self.website, groups=self.group, title="title", maximum='1')

        with self.assertRaisesMessage(ValidationError, "Maximum needs be positive integer - type received: " +
                                      str(type(1.1))):
            Options.objects.create(websites=self.website, groups=self.group, title="title", maximum=1.1)

        with self.assertRaisesMessage(ValidationError, "Minimum can't be negative"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", minimum=-1)

        with self.assertRaisesMessage(ValidationError, "Maximum can't be negative or zero"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", maximum=-1)

        with self.assertRaisesMessage(ValidationError, "Maximum can't be negative or zero"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", maximum=0)

        with self.assertRaisesMessage(ValidationError, "Minimum can't be greater than the maximum"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", minimum=2)

        with self.assertRaisesMessage(ValidationError, "Options' maximum can't be greater than Groups' maximum"):
            Options.objects.create(websites=self.website, groups=self.group, title="title", maximum=2)

