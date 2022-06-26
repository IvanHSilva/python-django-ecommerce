from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False, widget=forms.PasswordInput(), label='Senha:')

    passconf = forms.CharField(
        required=False, widget=forms.PasswordInput(), label='Confirmação da senha:')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'passconf', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        userdata = cleaned.get('username')
        emaildata = cleaned.get('email')
        passworddata = cleaned.get('password')
        passconfdata = cleaned.get('passconf')

        usersys = User.objects.filter(username=userdata).first()
        emailsys = User.objects.filter(email=emaildata).first()

        error_msg_user_exists = 'Usário já cadastrado'
        error_msg_email_exists = 'E-Mail já cadastrado'
        error_msg_pass_match = 'Senha não confere'
        error_msg_pass_short = 'Senha pequena, menos de 6 caracteres'
        error_msg_pass_required = 'Senha deve ser digitada'

        if self.user:
            if userdata != usersys:
                if usersys:
                    validation_error_msgs['username'] = error_msg_user_exists

            if emaildata != emailsys:
                if emailsys:
                    validation_error_msgs['email'] = error_msg_email_exists

            if passworddata != passconfdata:
                validation_error_msgs['password'] = error_msg_pass_match
                validation_error_msgs['passconf'] = error_msg_pass_match

            if len(passconfdata) < 6:
                validation_error_msgs['password'] = error_msg_pass_short

        else:
            if usersys:
                validation_error_msgs['username'] = error_msg_user_exists

            if emailsys:
                validation_error_msgs['email'] = error_msg_email_exists

            if not passworddata:
                validation_error_msgs['password'] = error_msg_pass_required

            if not passconfdata:
                validation_error_msgs['passconf'] = error_msg_pass_required

            if passworddata != passconfdata:
                validation_error_msgs['password'] = error_msg_pass_match
                validation_error_msgs['passconf'] = error_msg_pass_match

            if len(passconfdata) < 6:
                validation_error_msgs['password'] = error_msg_pass_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
