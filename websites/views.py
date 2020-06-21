from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from . import models


class Home(View):

    def get(self, *args, **kwargs):

        # SQL Queries
        websites = models.Websites.objects.filter(url=kwargs['url'])[:1][0]
        categories = models.Categories.objects.filter(websites=websites)
        products = models.Products.objects.filter(websites=websites, is_highlight=True)
        banners = models.Banners.objects.filter(websites=websites)

        context = {
            'websites': websites,
            'categories': categories or '',
            'products': products or '',
            'banners': banners or ''
        }

        return render(self.request, 'website.html', context)
