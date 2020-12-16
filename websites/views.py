from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors


def website_configs(website):
    pass


def list_product(**kwargs):
    """
    There are 3 ways to list the products, 1 by category, 2 by the search bar, 3 by accessing the homepage.
    """
    if kwargs['category']:
        return Products.objects.filter(categories=kwargs['category']).order_by('position')
    if kwargs['search']:
        return Products.objects.filter(websites=kwargs['websites'],
                                       title__icontains=kwargs['search']).order_by('position')

    return Products.objects.filter(websites=kwargs['websites'],
                                   show_home=True).order_by('position')


class Home(View):

    def get(self, *args, **kwargs):

        website = get_object_or_404(Websites, url=kwargs['url'])

        contact = Contacts.objects.filter(websites=website).first()
        icon = Icons.objects.filter(websites=website).first()
        color = Colors.objects.filter(websites=website).first()

        banners = Banners.objects.filter(websites=website).order_by('position')
        categories = Categories.objects.filter(websites=website).order_by('position')

        category = ''
        search = self.request.GET.get('search')

        if 'category' in kwargs:
            category = Categories.objects.filter(websites=website, slug=kwargs['category']).first()

        products = list_product(websites=website, category=category, search=search)

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'websites': website,
            'contacts': contact,
            'icons': icon,
            'colors': color,
            'banners': banners,
            'categories': categories,
            'category_': category,
            'products': page_obj,
        }

        return render(self.request, 'website.html', context)


class Product(View):

    def get(self, *args, **kwargs):

        websites = Websites.objects.get(url=kwargs['url'])
        icons = Icons.objects.get(websites=websites)
        colors = Colors.objects.get(websites=websites)
        product = Products.objects.get(websites=websites, slug=kwargs['product'])
        groups = Groups.objects.filter(products=product).order_by('position')
        options = Options.objects.filter(groups__in=groups).order_by('position')

        context = {
            'websites': websites,
            'icons': icons or '',
            'colors': colors or '',
            'product': product or '',
            'groups': groups or '',
            'options': options or ''
        }

        return render(self.request, 'website.html', context)

    def post(self, *args, **kwargs):

            websites = Websites.objects.get(url=kwargs['url'])
            icons = Icons.objects.get(websites=websites)
            colors = Colors.objects.get(websites=websites)
            product = Products.objects.get(websites=websites, slug=kwargs['product'])
            groups = Groups.objects.filter(products=product).order_by('position')
            options = Options.objects.filter(groups__in=groups).order_by('position')

            context = {
                'websites': websites,
                'icons': icons or '',
                'colors': colors or '',
                'product': product or '',
                'groups': groups or '',
                'options': options or ''
            }

            return render(self.request, 'website.html', context)


class Cart(View):

    def get(self, *args, **kwargs):
        ...
