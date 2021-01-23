from ..models import Websites, Colors, Icons, Banners, Contacts, Categories, Products, Groups, Options

"""
Here are the test scenarios
"""


def check_info():
    """
    This scenario was created to check website information, so we'll add contact, 6 categories
    """

    website = Websites.objects.create(url='checkinfo', title="Check Info")

    for x in range(6):
        Categories.objects.create(websites=website, title=f'Category {x+1}')

    Contacts.objects.create(websites=website, telephone='7873923408', email='checkinfo@gmail.com',
                            facebook='checkinfofacebook', instagram='checkinfoinstagram', twitter='checkinfotwitter',
                            linkedin='checkinfolinkedin', pinterest='checkinfopinterest', youtube='checkinfoyoutube',
                            whatsapp='7873923408', social_media_text='Follow us :D', whatsapp_text='Whatsapp:')


def colors():
    """
    This scenario was created to check whether colors is working, so we'll add colors for the website
    """

    website = Websites.objects.create(url='colors', title="Colors")

    Colors.objects.create(websites=website, navbar='FF44E7', category='FF4444', active='7044FF', footer='44F8FF',
                          text='44FFA8', title='FCFF44', title_hover='D50E04')

    category = Categories.objects.create(websites=website, title="Category 1")

    Products.objects.create(websites=website, categories=category, title="Product", price=1000)


def images():
    """
    This scenario was created to check whether images is working, so we'll use icons and banners for the website
    """

    website = Websites.objects.create(url='images', title="Images")

    Icons.objects.create(websites=website, shortcut='images/shortcut.png', account='images/account.png',
                         cart='images/cart.png', search='images/search.png', home='images/home.png')

    Banners.objects.create(websites=website, images='images/banner-1.jpg')

    Banners.objects.create(websites=website, images='images/banner-2.jpg')

    Categories.objects.create(websites=website, title="Category 1")


def products():
    """
    The scenario created to test list product, with a website, 4 categories, 27 products for the first two categories,
    9 products has promotional price and 9 products without price (price_type=3). Also is tested the 'available'
    and 'show_home' field. The promotional price test the floating point problem.
    """
    website = Websites.objects.create(url='products', title="Products")

    categories = []

    for x in range(4):
        categories.append(Categories.objects.create(websites=website, title=f"Category {x+1}"))

    for x in range(9):
        Products.objects.create(websites=website, categories=categories[0],
                                title=f'{categories[0].title} Product {x+1}', price=x+1)

        Products.objects.create(websites=website, categories=categories[0],
                                title=f'{categories[0].title} Promotional {x+1}', price=x+1,
                                promotional_price=float(f'{x}.{x}'))

        Products.objects.create(websites=website, categories=categories[0],
                                title=f'{categories[0].title} Price type 3 {x+1}', price_type='3')

        Products.objects.create(websites=website, categories=categories[1], show_on_home=False,
                                title=f'{categories[1].title} Product {x+1}', price=x+1)

        Products.objects.create(websites=website, categories=categories[1], show_on_home=False,
                                title=f'{categories[1].title} Promotional {x+1}', price=x+1,
                                promotional_price=float(f'{x}.{x}'))

        Products.objects.create(websites=website, categories=categories[1], show_on_home=False,
                                title=f'{categories[1].title} Price type 3 {x+1}', price_type='3')


def product_type(price_type):

    price = 30000 if price_type != '3' else None

    website = Websites.objects.create(url='products', title="Products")

    category = Categories.objects.create(websites=website, title="Category")

    product = Products.objects.create(websites=website, categories=category, title=f'Product',
                                      price=price, price_type=price_type)

    size = ((1, 1), (0, 1), (0, 10))

    if price_type != '1':
        price_type = '1'
        price = 200
    else:
        price_type = None
        price = None

    for x in range(3):

        group = Groups.objects.create(websites=website, products=product, title=f'group {x + 1}',
                                      maximum=size[x][1], minimum=size[x][0], price_type=price_type)

        for y in range(3):
            Options.objects.create(websites=website, groups=group, title=f'option {y+1}', price=price,
                                   maximum=size[x][1], minimum=0)

        if x > 0:
            Options.objects.create(websites=website, groups=group, title="Readonly", maximum=size[x][1],
                                   minimum=size[x][1], price=price)
