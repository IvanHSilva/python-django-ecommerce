from itertools import product
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from .models import Product


class ListProduct(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 3


class DetailsProduct(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetailsProduct')


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddToCart')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class CartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CartView')


class FinalizeCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogoutProfile')
