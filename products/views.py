from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, ProdVariation
from pprint import pprint


class ListProduct(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 3
    ordering = ['id']


class DetailsProduct(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        # messages.success(self.request, 'Sucesso!!! (SQN....)')
        # return redirect(self.request.META['HTTP_REFERER'])

        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        referer = self.request.META.get(
            'HTTP_REFERER', reverse('products:list'))
        vid = self.request.GET.get('vid')

        if not vid:
            messages.error(self.request, 'Produto não existe')
            return redirect(referer)

        variation = get_object_or_404(ProdVariation, id=vid)
        varstock = variation.stock
        product = variation.product

        prodid = product.id
        prodname = product.name
        varname = variation.name or ''
        price = variation.price
        promo = variation.promoprice
        quant = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if vid in cart:
            cartquant = cart[vid]['quant']
            cartquant += 1

            if varstock < cartquant:
                messages.warning(
                    self.request, 'Estoque insuficiente do produto')
                cartquant = varstock
                cart[vid]['quant'] = cartquant
                cart[vid]['pricequant'] = price * cartquant
                cart[vid]['promoquant'] = promo * cartquant

        else:
            cart[vid] = {
                'prodid': prodid,
                'prodname': prodname,
                'varid': vid,
                'varname': varname,
                'price': price,
                'promo': promo,
                'quant': 1,
                'slug': slug,
                'image': image
            }
        self.request.session.save()
        # pprint(cart)
        # return HttpResponse(f'{variation.product} {variation.name}')
        messages.success(
            self.request, f'Adicionado ao carrinho {cart[vid]["quant"]}x')
        return redirect(referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        referer = self.request.META.get(
            'HTTP_REFERER', reverse('products:list'))
        vid = self.request.GET.get('vid')

        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        if not vid:
            print('sem vid')
            return redirect(referer)

        if not self.request.session.get('cart'):
            print('sem carrinho')
            return redirect(referer)

        if vid not in self.request.session['cart']:
            print(f'sem sessão {vid} {self.request.session["cart"]}')
            return redirect(referer)

        cart = self.request.session['cart'][vid]
        print(cart)

        messages.success(self.request,
                         f'Produto {cart["prodname"]} foi removido com sucesso!')
        # del cart
        del self.request.session['cart'][vid]
        self.request.session.save()

        return redirect(referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'products/cart.html', context)


class FinalizeCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogoutProfile')
