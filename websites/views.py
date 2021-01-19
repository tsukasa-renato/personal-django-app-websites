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


def check_request(request, website):

    product = get_object_or_404(Products, pk=request['product'])

    if product.websites != website:
        return HttpResponseBadRequest("Bad Request")

    product = {
        'model': product,
        'quantity': 1,
        'total': product.get_real_price() if product.get_real_price() else 0,
        'groups': []
    }

    aux = get_product_groups_options({'product': product['model']})

    for option in aux['options']:

        group = str(option.groups).replace('-', '')

        if group not in aux:
            aux[group] = {
                'options': [],
                'total': 0,
                'quantity': 0
            }

        if option.check_input_type() == 'radio':

            keyword = group

            if keyword in request:

                if request[keyword] != str(option.pk):
                    return HttpResponseBadRequest("Bad Request")

                aux[group]['options'].append({
                    'model': option,
                    'quantity': 1,
                })

                aux[group]['quantity'] += 1
                aux[group]['total'] += option.get_real_price() if option.get_real_price() else 0

        else:

            keyword = f'{option.pk}'

            if option.check_input_type() == 'checkbox':

                if keyword in request:

                    if request[keyword] != str(option.pk):
                        return HttpResponseBadRequest("Bad Request")

                    aux[group]['options'].append({
                        'model': option,
                        'quantity': 1,
                    })

                    aux[group]['quantity'] += 1
                    aux[group]['total'] += option.get_real_price() if option.get_real_price() else 0

            elif option.check_input_type() == 'number':

                if keyword in request:

                    quantity = int(request[keyword])

                    if option.minimum > quantity or quantity > option.maximum:
                        return HttpResponseBadRequest("Bad Request")

                    if quantity > 0:
                        aux[group]['options'].append({
                            'model': option,
                            'quantity': quantity,
                        })

                        aux[group]['quantity'] += 1
                        aux[group]['total'] += option.get_real_price() * quantity if option.get_real_price() else 0

            if keyword not in request:

                if option.minimum > 0:
                    return HttpResponseBadRequest("Bad Request")

    for group in aux['groups']:

        keyword = str(group).replace('-', '')

        if aux[keyword]['quantity'] < group.minimum or aux[keyword]['quantity'] > group.maximum:
            return HttpResponseBadRequest("Bad Request")

        if group.price_type == '2':
            aux[keyword]['total'] /= aux[keyword]['quantity']

        product['groups'].append({
            'model': group,
            'options': aux[keyword]['options'],
        })

        product['total'] += aux[keyword]['total']

    return product


class Cart(View):

    def post(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        context['cart'] = {
            'products': [],
            'quantity': 0,
            'total': 0
        }

        product = check_request(self.request.POST, context['website'])

        context['cart']['products'].append(product)
        context['cart']['total'] += product['total']
        context['cart']['quantity'] += product['quantity']

        return render(self.request, 'website.html', context)
