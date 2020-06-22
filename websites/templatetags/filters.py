from django import template
from utils import utils

register = template.Library()


@register.filter
def mine_less(number):
    return number - 1


@register.filter
def money_format(money):
    return utils.money_format(money)
