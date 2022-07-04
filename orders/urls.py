from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('',  views.ListOrder.as_view(), name='list'),
    path('pay/<int:pk>', views.PayOrder.as_view(), name='pay'),
    path('save/', views.SaveOrder.as_view(), name='save'),
    # path('list/', views.ListOrder.as_view(), name='list'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detail'),
]
