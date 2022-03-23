from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class CreateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CreateProfile')


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('UpdateProfile')


class LoginProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LoginProfile')


class LogoutProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('LogoutProfile')
