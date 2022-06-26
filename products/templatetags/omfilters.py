from atexit import register
from django.template import Library
from utils import utils

register = Library()


@register.filter
def formatprice(price):
    return utils.formatprice(price)


@register.filter
def quanttotalcart(cart):
    return utils.quanttotalcart(cart)


@register.filter
def totalcart(cart):
    return utils.totalcart(cart)
