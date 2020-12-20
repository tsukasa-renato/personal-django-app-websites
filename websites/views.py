from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors


def list_product(website, category, search):
    """
    There are 4 ways to list the products, 1 by category and search bar, 2 by category, 3 by the search bar,
    4 by accessing the homepage.
    """

    if category and search:
        return Products.objects.filter(websites=website, categories=category,
                                       title__icontains=search).order_by('position')

    if category:
        return Products.objects.filter(categories=category).order_by('position')
    if search:
        return Products.objects.filter(websites=website,
                                       title__icontains=search).order_by('position')

    return Products.objects.filter(websites=website,
                                   show_home=True).order_by('position')


class Home(View):

    def get(self, *args, **kwargs):

        website = get_object_or_404(Websites, url=kwargs['url'])

        contact = Contacts.objects.filter(websites=website).first()
        icon = Icons.objects.filter(websites=website).first()
        color = Colors.objects.filter(websites=website).first()

        banners = Banners.objects.filter(websites=website).order_by('position')
        categories = Categories.objects.filter(websites=website).order_by('position')

        search = self.request.GET.get('search')

        if 'category_selected' in kwargs:
            category_selected = Categories.objects.filter(websites=website, slug=kwargs['category_selected']).first()
        else:
            category_selected = False

        products = list_product(website=website, category=category_selected, search=search)

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'website': website,
            'contact': contact,
            'icon': icon,
            'color': color,
            'banners': banners,
            'categories': categories,
            'category_selected': category_selected,
            'products': page_obj,
        }

        return render(self.request, 'website.html', context)


class Product(View):

    def get(self, *args, **kwargs):
        website = get_object_or_404(Websites, url=kwargs['url'])

        contact = Contacts.objects.filter(websites=website).first()
        icon = Icons.objects.filter(websites=website).first()
        color = Colors.objects.filter(websites=website).first()

        product = Products.objects.get(websites=website, slug=kwargs['product'])
        groups = Groups.objects.filter(products=product).order_by('position')
        options = Options.objects.filter(groups__in=groups).select_related('groups').order_by('position')

        context = {
            'website': website,
            'icon': icon,
            'color': color,
            'product': product,
            'groups': groups,
            'options': options,
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
