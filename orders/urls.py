from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.PayOrder.as_view(), name='pay'),
    path('close/', views.CloseOrder.as_view(), name='close'),
    path('detail/', views.DetailOrder.as_view(), name='login'),
]
