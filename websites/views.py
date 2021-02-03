from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View
from django.core.paginator import Paginator
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors
from django.http import HttpResponseBadRequest
from decimal import Decimal


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

    context['product'] = get_object_or_404(Products, websites=context['website'], is_available=True,
                                           slug=context['selected_product'])
    context['groups'] = Groups.objects.filter(products=context['product']).order_by('position')
    context['options'] = Options.objects.filter(groups__in=context['groups']).select_related('groups').order_by(
        'position')

    return context


def check_request_for_cart(request, context):

    context = get_product_groups_options({
            'selected_product': request['product'],
            'website': context['website'],
         })

    if context['product'].websites != context['website']:
        return HttpResponseBadRequest("Bad Request")

    total = context['product'].get_real_price() if context['product'].get_real_price() else 0

    product = {
        'images': context['product'].images.url if context['product'].images else '',
        'title': context['product'].title,
        'slug': context['product'].slug,
        'quantity': 1,
        'price': str(context['product'].get_real_price()) if context['product'].get_real_price() else '',
        'groups': []
    }

    for option in context['options']:

        group = str(option.groups).replace('-', '')

        if group not in context:
            context[group] = {
                'options': [],
                'total': 0,
                'quantity': 0
            }

        quantity = 0

        if option.check_input_type() == 'radio':

            keyword = group

            quantity = 1 if request[keyword] == str(option.pk) else 0

        else:

            keyword = f'{option.pk}'

            if keyword in request:

                if option.check_input_type() == 'checkbox':

                    if request[keyword] != str(option.pk):
                        return HttpResponseBadRequest("Bad Request")

                    quantity = 1

                else:

                    quantity = int(request[keyword])

                    if option.minimum > quantity or quantity > option.maximum:
                        return HttpResponseBadRequest("Bad Request")

        if quantity > 0:

            context[group]['options'].append({
                'image': option.images.url if option.images else '',
                'title': option.title,
                'price': str(option.get_real_price()) if option.get_real_price() else '',
                'quantity': quantity,
            })

            context[group]['quantity'] += quantity
            context[group]['total'] += option.get_real_price() * quantity if option.get_real_price() else 0

        else:

            if option.minimum > 0:
                return HttpResponseBadRequest("Bad Request")

    for group in context['groups']:

        keyword = str(group).replace('-', '')

        if context[keyword]['quantity'] < group.minimum or context[keyword]['quantity'] > group.maximum:
            return HttpResponseBadRequest("Bad Request")

        if group.price_type == '2':
            context[keyword]['total'] /= context[keyword]['quantity']

        product['groups'].append({
            'title': group.title,
            'options': context[keyword]['options'],
        })

        total += context[keyword]['total']
        context[keyword]['total'] = str(context[keyword]['total'])

    product['total'] = str(total)

    print(product)

    return product


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

        if 'cart' in self.request.session:
            context['cart'] = {'quantity': self.request.session['cart']['quantity']}

        return render(self.request, 'website.html', context)


class ShowProduct(View):

    def get(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        context['selected_product'] = str(kwargs['selected_product'])

        context = get_product_groups_options(context)

        if 'cart' in self.request.session:
            context['cart'] = {'quantity': self.request.session['cart']['quantity']}

        context['position'] = kwargs['position'] if 'position' in kwargs else ''

        return render(self.request, 'website.html', context)


class Cart(View):

    def get(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        if 'cart' in self.request.session:

            context['cart'] = self.request.session['cart']

        else:

            context['cart'] = {
                'products': [],
                'quantity': 0,
                'total': 0
            }

        return render(self.request, 'website.html', context)

    def post(self, *args, **kwargs):

        context = kwargs

        return render(self.request, 'website.html', context)


class CartActions(View):

    def get(self, *args, **kwargs):

        if 'cart' in self.request.session:

            if 'position' in kwargs and len(self.request.session['cart']['products']) > 0:

                self.request.session.modified = True

                position = int(kwargs['position'])
                product = self.request.session['cart']['products'][position]

                total = Decimal(self.request.session['cart']['total'])
                total -= Decimal(product['total'])

                self.request.session['cart']['total'] = str(total)
                self.request.session['cart']['quantity'] -= product['quantity']

                del self.request.session['cart']['products'][position]

        return redirect('websites:cart', url=kwargs['url'])

    def post(self, *args, **kwargs):

        context = {'url': str(kwargs['url'])}

        context = website_configs(context)

        if 'cart' not in self.request.session:
            self.request.session['cart'] = {
                'products': [],
                'quantity': 0,
            }

            total = 0
        else:
            self.request.session.modified = True
            total = Decimal(self.request.session['cart']['total'])

        product = check_request_for_cart(self.request.POST, context)

        if 'title' not in product:
            return HttpResponseBadRequest("Bad Request")

        if 'position' in self.request.POST:

            position = int(self.request.POST['position'])

            total -= Decimal(self.request.session['cart']['products'][position]['total'])
            self.request.session['cart']['quantity'] -= self.request.session['cart']['products'][position]['quantity']

            self.request.session['cart']['products'][position] = product

        else:

            self.request.session['cart']['products'].append(product)

        total += Decimal(product['total'])

        self.request.session['cart']['total'] = str(total)
        self.request.session['cart']['quantity'] += product['quantity']

        context['cart'] = self.request.session['cart']

        return redirect('websites:cart', url=context['url'])
