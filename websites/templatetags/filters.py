from django import template
from django.http import QueryDict

from utils import utils

register = template.Library()


@register.filter
def mine_less(number):
    return number - 1


@register.simple_tag
def money_format(money, currency):
    if currency == 'auto':
        return utils.money_format(money, '')
    return utils.money_format(money, currency)


@register.filter
def smartphone_format(number):
    return utils.smartphone_format(number)


@register.filter
def remove_dash(text):
    text = str(text)
    return text.replace('-', '')

