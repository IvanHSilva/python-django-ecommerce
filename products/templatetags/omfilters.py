from atexit import register
from django.template import Library
from utils import utils

register = Library()


@register.filter
def formatprice(price):
    return utils.formatprice(price)
