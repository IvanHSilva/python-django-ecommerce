from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import ProdVariation
from .models import Order, OrderItem
from utils import utils


class DispatchLoginRequired(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class PayOrder(DispatchLoginRequired, DetailView):
    template_name = 'orders/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'orders/save.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Faça o  login')
            return redirect('profiles:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Carrinho vazio')
            return redirect('products:list')

        cart = self.request.session.get('cart')
        cartvarids = [v for v in cart]
        # print(cart)
        variations = list(ProdVariation.objects.select_related(
            'product').filter(id__in=cartvarids))
        # print('Variações: ', variations)

        for var in variations:
            vid = str(var.id)
            stock = var.stock
            cartquant = cart[vid]['quant']
            pricequant = cart[vid]['price']
            promoquant = cart[vid]['promo']
            # print(var.product, stock, cartquant)

            msgstockerror = ''
            if stock < cartquant:
                cart[vid]['quant'] = stock
                cart[vid]['price'] = stock * pricequant
                cart[vid]['promoprice'] = stock * promoquant

                msgstockerror = 'Algumas quantidades de itens do seu carrinho foram alteradas devido a diferenças no estoque'

                if msgstockerror:
                    messages.warning(self.request, msgstockerror)

                self.request.session.save()
                return redirect('products:cart')

        quantity = utils.quanttotalcart(cart)
        total = utils.totalcart(cart)

        order = Order(
            user=self.request.user,
            quantity=quantity,
            total=total,
            status='C',
        )
        order.save()

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=v['prodname'],
                productid=v['prodid'],
                variation=v['varname'],
                variationid=v['varid'],
                price=v['price'],
                promoprice=v['promo'],
                quantity=v['quant'],
                image=v['image'],
            ) for v in cart.values()
        ])

        context = {}

        del self.request.session['cart']
        # return render(self.request, self.template_name, context)
        # return redirect('orders:list')
        return redirect(reverse('orders:pay', kwargs={'pk': order.pk}))
        # return HttpResponse('PayOrder')


class ListOrder(DispatchLoginRequired, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/list.html'
    paginate_by = 10
    ordering = ['-id']


class DetailOrder(DispatchLoginRequired, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/detail.html'
    pk_url_kwarg = 'pk'
