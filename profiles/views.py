from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from . import models
from . import forms

import copy


class BaseProfile(View):
    template_name = 'profiles/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Profile.objects.filter(
                user=self.request.user).first()
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        # return HttpResponse('CreateProfile')
        return self.render


class CreateProfile(BaseProfile):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            # if not self.userform.is_valid():
            messages.error(self.request, 'Erro nos dados! '
                           'Verifique se os campos abaixo foram preenchidos corretamente.')
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        firstname = self.userform.cleaned_data.get('first_name')
        lastname = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username
            if password:
                user.set_password(password)
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.Profile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            auth = authenticate(self.request, username=user, password=password)
            if auth:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()
        messages.success(self.request, 'Cadastro atualizado com sucesso.')
        return redirect('products:cart')
        return self.render


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('UpdateProfile')


class LoginProfile(View):
    def post(self, *args, **kwargs):
        # return HttpResponse('LoginProfile')
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
    # def get(self, *args, **kwargs):
    #     return HttpResponse('LoginProfile')
        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválidos!')
            return redirect('profiles:create')

        user = authenticate(self.request, username=username, password=password)
        if not user:
            messages.error(self.request, 'Usuário ou senha inválidos!')
            return redirect('profiles:create')

        login(self.request, user=user)
        messages.success(self.request, 'Usuário logado com sucesso!')
        return redirect('products:cart')


class LogoutProfile(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('products:list')
        # return HttpResponse('LogoutProfile')
