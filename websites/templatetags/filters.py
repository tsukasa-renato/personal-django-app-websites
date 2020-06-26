from django import template
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
