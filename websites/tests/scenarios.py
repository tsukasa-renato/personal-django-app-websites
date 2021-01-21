from ..models import Websites, Colors, Contacts, Categories, Products, Groups, Options

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


def create_scenario_1():
    """
    The scenario created for testing, with a website, contacts, four categories, 9 products for the first category,
    and 9 products for the second category
    """
    website = Websites.objects.create(url='website', title="Website")

    categories = [
        Categories.objects.create(websites=website, title="Category 1"),
        Categories.objects.create(websites=website, title="Category 2"),
        Categories.objects.create(websites=website, title="Category 3"),
        Categories.objects.create(websites=website, title="Category 4")
    ]

    contact = Contacts.objects.create(websites=website, telephone='7873923408', email='example@email.com',
                                      facebook='example', instagram='example', twitter='example', linkedin='example',
                                      whatsapp='7873923408')

    aux = (
        ("Product One", 10.2), ("Product Two", 10.2), ("Product Three", 10.2), ("Product Four", 10.2),
        ("Product Five", 10.2), ("Product Six", 10.2), ("Product Seven", 10.2), ("Product Eight", 10.2),
    )

    for product in aux:
        Products.objects.create(websites=website, categories=categories[0],
                                title=product[0], price=product[1])

    Products.objects.create(websites=website, categories=categories[0], title="Promotional",
                            price=10.2, promotional_price=5)

    aux = (
        ("One Product", 10.2), ("Two Product", 10.2), ("Three Product", 10.2), ("Four Product", 10.2),
        ("Five Product", 10.2), ("Six Product", 10.2), ("Seven Product", 10.2), ("Eight Product", 10.2),
    )

    for product in aux:
        Products.objects.create(websites=website, categories=categories[1], title=product[0],
                                price=product[1], show_on_home=False)

    Products.objects.create(websites=website, categories=categories[1], title="Promotional2",
                            price=10.2, promotional_price=5, show_on_home=False)

    return website, contact, categories


def create_scenario_2():

    website = Websites.objects.create(url='website2', title="Website")
    category = Categories.objects.create(websites=website, title="Category")

    product_price = 30000
    option_price = None
    group_type = None

    for x in range(3):

        if x > 0:
            option_price = 200
            group_type = '1'

        if x == 2:
            product_price = None

        product = Products.objects.create(websites=website, categories=category, title=f'Product{x+1}',
                                          description=f'Product with price type {x+1}',
                                          price=product_price, price_type=str(x+1))

        groups = (
            ('radio group', 1, 1), ('checkbox group', 1, 0), ('numbers group', 5, 0),
        )

        for group in groups:
            g = Groups.objects.create(websites=website, products=product, title=group[0],
                                      maximum=group[1], minimum=group[2], price_type=group_type)

            for y in range(3):
                Options.objects.create(websites=website, groups=g, title=f'Op{y+1}', maximum=group[1],
                                       price=option_price)

            Options.objects.create(websites=website, groups=g, title="Readonly", maximum=group[1], minimum=group[1],
                                   price=option_price)

    return website, category

