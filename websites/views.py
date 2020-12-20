from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors


class Website(TemplateView):

    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            self.website = get_object_or_404(Websites, url=kwargs['url'])
            self.contact = Contacts.objects.filter(websites=self.website).first()
            self.icon = Icons.objects.filter(websites=self.website).first()
            self.color = Colors.objects.filter(websites=self.website).first()
            self.categories = Categories.objects.filter(websites=self.website).order_by('position')


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


class Home(Website):

    template_name = "website.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        super().__init__(self, **kwargs)

        context['banners'] = Banners.objects.filter(websites=self.website).order_by('position')

        search = self.request.GET.get('search')

        if 'category_selected' in kwargs:
            category = Categories.objects.filter(websites=self.website, slug=kwargs['category_selected']).first()
        else:
            category = False

        products = list_product(website=self.website, category=category, search=search)

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['website'] = self.website
        context['icon'] = self.icon
        context['color'] = self.color
        context['categories'] = self.categories
        context['products'] = page_obj
        context['contact'] = self.contact

        return context


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
            'contact': contact,
            'icon': icon,
            'color': color,
            'product': product,
            'groups': groups,
            'options': options,
        }

        return render(self.request, 'website.html', context)


class Cart(View):

    def get(self, *args, **kwargs):
        ...
