from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('', views.CreateProfile.as_view(), name='create'),
    path('update/', views.UpdateProfile.as_view(), name='update'),
    path('login/', views.LoginProfile.as_view(), name='login'),
    path('logout/', views.LogoutProfile.as_view(), name='logout'),
]
