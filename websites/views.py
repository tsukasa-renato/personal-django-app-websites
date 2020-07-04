from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from . import models


class Home(View):

    def get(self, *args, **kwargs):

        category = ''
        search = self.request.GET.get('search')

        websites = models.Websites.objects.filter(url=kwargs['url']).first()
        contacts = models.Contacts.objects.filter(websites=websites).first()
        icons = models.Icons.objects.filter(websites=websites).first()
        colors = models.Colors.objects.filter(websites=websites).first()
        banners = models.Banners.objects.filter(websites=websites).order_by('position')
        categories = models.Categories.objects.filter(websites=websites).order_by('position')

        if 'category' in kwargs:
            category = models.Categories.objects.filter(websites=websites, slug=kwargs['category']).first()

        if category:
            products = models.Products.objects.filter(websites=websites, categories=category).order_by('position')
        elif search:
            products = models.Products.objects.filter(websites=websites,
                                                      title__icontains=search).order_by('position')
        else:
            products = models.Products.objects.filter(websites=websites, show_home=True).order_by('position')

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
