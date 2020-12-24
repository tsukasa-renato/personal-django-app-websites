from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors
from django.http import HttpResponse


def list_products(website, category, search):
    """
    There are 3 ways to list the products, 1 by category, 2 by the search bar, 3 by accessing the homepage.
    """

    if search:
        return Products.objects.filter(websites=website,
                                       title__icontains=search).order_by('position')
    if category:
        category = get_object_or_404(Categories, websites=website, slug=category)
        return Products.objects.filter(categories=category).order_by('position')

    return Products.objects.filter(websites=website,
                                   show_on_home=True).order_by('position')


class Website(TemplateView):

    template_name = "website.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['website'] = get_object_or_404(Websites, url=kwargs['url'])
        context['contact'] = Contacts.objects.filter(websites=context['website']).first()
        context['icon'] = Icons.objects.filter(websites=context['website']).first()
        context['color'] = Colors.objects.filter(websites=context['website']).first()
        context['categories'] = Categories.objects.filter(websites=context['website']).order_by('position')

        return context


class ShowProducts(Website):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['banners'] = Banners.objects.filter(websites=context['website']).order_by('position')

        category = context['selected_category'] if 'selected_category' in context else ''
        search = self.request.GET.get('search')

        products = list_products(website=context['website'], category=category, search=search)

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)

        return context


class ShowProduct(Website):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Products, websites=context['website'], slug=context['selected_product'])
        context['groups'] = Groups.objects.filter(products=context['product']).order_by('position')
        context['options'] = Options.objects.filter(groups__in=context['groups']).select_related('groups').order_by(
            'position')

        return context


class Cart(View):

    def post(self, request):

        return HttpResponse("<h1>In development</h1>")
