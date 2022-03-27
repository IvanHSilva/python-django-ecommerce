from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.ListProduct.as_view(), name='list'),
    path('<slug>', views.DetailsProduct.as_view(), name='detail'),
    path('addcart/', views.AddToCart.as_view(), name='addcart'),
    path('removcart/', views.RemoveFromCart.as_view(), name='removcart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('finalize/', views.FinalizeCart.as_view(), name='finalize'),
]
