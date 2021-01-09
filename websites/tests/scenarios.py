from ..models import Websites, Contacts, Categories, Products, Groups, Options
from django.core.paginator import Paginator


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

    products = Products.objects.filter(websites=website, is_available=True, show_on_home=True).order_by('position')
    products = Paginator(products, 8)

    return website, contact, categories, products

