from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from . import models


def list_product(**kwargs):
    """
    There are 3 ways to list the products, 1 by category, 2 by the search bar, 3 by accessing the homepage.
    """
    if kwargs['category']:
        return models.Products.objects.filter(categories=kwargs['category']).order_by('position')
    if kwargs['search']:
        return models.Products.objects.filter(websites=kwargs['websites'],
                                              title__icontains=kwargs['search']).order_by('position')

    return models.Products.objects.filter(websites=kwargs['websites'],
                                          show_home=True).order_by('position')


class Home(View):

    def get(self, *args, **kwargs):

        websites = models.Websites.objects.get(url=kwargs['url'])
        contacts = models.Contacts.objects.get(websites=websites)
        icons = models.Icons.objects.get(websites=websites)
        colors = models.Colors.objects.get(websites=websites)
        banners = models.Banners.objects.filter(websites=websites).order_by('position')
        categories = models.Categories.objects.filter(websites=websites).order_by('position')

        category = ''
        search = self.request.GET.get('search')

        if 'category' in kwargs:
            category = models.Categories.objects.filter(websites=websites, slug=kwargs['category']).first()

        products = list_product(websites=websites, category=category, search=search)

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'websites': websites,
            'contacts': contacts or '',
            'icons': icons or '',
            'colors': colors or '',
            'banners': banners or '',
            'categories': categories or '',
            'category_': category or '',
            'products': page_obj or '',
        }

        return render(self.request, 'website.html', context)


class Product(View):

    def get(self, *args, **kwargs):

        websites = models.Websites.objects.get(url=kwargs['url'])
        icons = models.Icons.objects.get(websites=websites)
        colors = models.Colors.objects.get(websites=websites)
        product = models.Products.objects.get(websites=websites, slug=kwargs['product'])
        groups = models.Groups.objects.filter(products=product).order_by('position')
        options = models.Options.objects.filter(groups__in=groups).order_by('position')

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

            websites = models.Websites.objects.get(url=kwargs['url'])
            icons = models.Icons.objects.get(websites=websites)
            colors = models.Colors.objects.get(websites=websites)
            product = models.Products.objects.get(websites=websites, slug=kwargs['product'])
            groups = models.Groups.objects.filter(products=product).order_by('position')
            options = models.Options.objects.filter(groups__in=groups).order_by('position')

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
