from django import template

register = template.Library()


@register.filter
def mine_less(number):
    return number - 1


def money_format(money):
    return
