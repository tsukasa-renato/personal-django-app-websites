from django import template

from websites.utils import utils

register = template.Library()


@register.filter
def mine_less(number):
    return number - 1


@register.simple_tag
def money_format(money, currency, language):
    return utils.money_format(money, currency, language)


@register.filter
def smartphone_format(number):
    return utils.smartphone_format(number)

