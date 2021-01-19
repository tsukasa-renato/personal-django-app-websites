from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors
from django.http import HttpResponseBadRequest


def website_configs(context):

    context['website'] = get_object_or_404(Websites, url=context['url'])
    context['icon'] = Icons.objects.filter(websites=context['website']).first()
    context['color'] = Colors.objects.filter(websites=context['website']).first()
    context['contact'] = Contacts.objects.filter(websites=context['website']).first()
    context['categories'] = Categories.objects.filter(websites=context['website']).order_by('position')

    return context


def list_products(website, category, search):
    """
    There are 3 ways to list the products, 1 by category, 2 by the search bar, 3 by accessing the homepage.
    """

    if search:
        return Products.objects.filter(websites=website, is_available=True,
                                       title__icontains=search).order_by('position')
    if category:
        category = get_object_or_404(Categories, websites=website, slug=category)
        return Products.objects.filter(categories=category, is_available=True).order_by('position')

    return Products.objects.filter(websites=website, is_available=True,
                                   show_on_home=True).order_by('position')


def get_product_groups_options(context):

    context['groups'] = Groups.objects.filter(products=context['product']).order_by('position')
    context['options'] = Options.objects.filter(groups__in=context['groups']).select_related('groups').order_by(
        'position')

    return context


class ShowProducts(View):

    def get(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)
        context['banners'] = Banners.objects.filter(websites=context['website']).order_by('position')

        context['selected_category'] = str(kwargs['selected_category']) if 'selected_category' in kwargs else ''
        search = self.request.GET.get('search')

        context['products'] = list_products(website=context['website'], category=context['selected_category'],
                                            search=search)

        if context['products']:
            paginator = Paginator(context['products'], 8)
            page_number = self.request.GET.get('page')
            context['products'] = paginator.get_page(page_number)

        return render(self.request, 'website.html', context)


class ShowProduct(View):

    def get(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        slug = str(kwargs['selected_product'])
        context['product'] = get_object_or_404(Products, websites=context['website'], is_available=True, slug=slug)

        context = get_product_groups_options(context)

        return render(self.request, 'website.html', context)


class Cart(View):

    def post(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        request = self.request.POST

        aux = {'product': get_object_or_404(Products, pk=request['product'])}

        if aux['product'].websites != context['website']:
            return HttpResponseBadRequest("Bad Request")

        context['cart'] = {}

        context['cart']['product'] = {
            'image': aux['product'].images.url if aux['product'].images else '',
            'title': aux['product'].title,
            'quantity': 1,
            'price': aux['product'].get_real_price() if aux['product'].get_real_price() else '',
            'total': aux['product'].get_real_price() if aux['product'].get_real_price() else 0,
        }

        aux = get_product_groups_options(aux)

        for option in aux['options']:

            group = str(option.groups)

            if group not in context['cart']:
                context['cart'][group] = []
                aux[group] = 0

            if option.check_input_type() == 'radio':

                keyword = f'{option.groups}'

                if keyword in request:

                    if request[keyword] != str(option.pk):
                        return HttpResponseBadRequest("Bad Request")

                    context['cart'][group].append({
                        'image': option.images.url if option.images else '',
                        'title': option.title,
                        'price': option.get_real_price() if option.get_real_price() else '',
                        'quantity': 1,
                    })

                    aux[group] += 1
                    context['cart']['product']['total'] += option.get_real_price() if option.get_real_price() else 0

            else:

                keyword = f'{option.pk}'

                if option.check_input_type() == 'checkbox':

                    if keyword in request:

                        if request[keyword] != str(option.pk):
                            return HttpResponseBadRequest("Bad Request")

                        context['cart'][group].append({
                            'image': option.images.url if option.images else '',
                            'title': option.title,
                            'price': option.get_real_price() if option.get_real_price() else '',
                            'quantity': 1,
                        })

                        aux[group] += 1
                        context['cart']['product']['total'] += option.get_real_price() if option.get_real_price() else 0

                elif option.check_input_type() == 'number':

                    if keyword in request:

                        quantity = int(request[keyword])

                        if option.minimum > quantity or quantity > option.maximum:
                            return HttpResponseBadRequest("Bad Request")

                        if quantity > 0:
                            context['cart'][group].append({
                                'image': option.images.url if option.images else '',
                                'title': option.title,
                                'price': option.get_real_price() if option.get_real_price() else '',
                                'quantity': quantity,
                            })

                            aux[group] += quantity
                            context['cart']['product']['total'] += (option.get_real_price() * quantity) \
                                if option.get_real_price() else 0

                if keyword not in request:

                    if option.minimum > 0:
                        return HttpResponseBadRequest("Bad Request")

        context['cart']['groups'] = []

        for group in aux['groups']:

            keyword = str(group)

            if aux[keyword] < group.minimum or aux[keyword] > group.maximum:
                return HttpResponseBadRequest("Bad Request")

            context['cart']['groups'].append({
                'title': group.title,
                'slug': group.slug,
                'options': context['cart'][group.slug],
            })

        if 'cart-quantity' not in context:
            context['cart_quantity'] = 0

        if 'total' not in context['cart']:
            context['cart']['total'] = 0

        context['cart_quantity'] += 1
        context['cart']['total'] += context['cart']['product']['total']

        return render(self.request, 'website.html', context)
