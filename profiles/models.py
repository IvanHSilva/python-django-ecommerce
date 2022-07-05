from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validatecpf import validatecpf
import re


class Profile(models.Model):
    user = models.OneToOneField(
        User, verbose_name='usuário', on_delete=models.DO_NOTHING)
    birthdate = models.DateField(verbose_name='data de nascimento')
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    address = models.CharField(verbose_name='endereço', max_length=60)
    addnumber = models.CharField(verbose_name='número', max_length=5)
    district = models.CharField(verbose_name='bairro', max_length=30)
    city = models.CharField(verbose_name='cidade', max_length=40)
    state = models.CharField(verbose_name='estado', max_length=2, default='SP',
                             choices=(
                                 ('AC', 'Acre'),
                                 ('AL', 'Alagoas'),
                                 ('AP', 'Amapá'),
                                 ('AM', 'Amazonas'),
                                 ('BA', 'Bahia'),
                                 ('CE', 'Ceará'),
                                 ('DF', 'Distrito Federal'),
                                 ('ES', 'Espírito Santo'),
                                 ('GO', 'Goiás'),
                                 ('MA', 'Maranhão'),
                                 ('MT', 'Mato Grosso'),
                                 ('MS', 'Mato Grosso do Sul'),
                                 ('MG', 'Minas Gerais'),
                                 ('PA', 'Pará'),
                                 ('PB', 'Paraíba'),
                                 ('PR', 'Paraná'),
                                 ('PE', 'Pernambuco'),
                                 ('PI', 'Piauí'),
                                 ('RJ', 'Rio de Janeiro'),
                                 ('RN', 'Rio Grande do Norte'),
                                 ('RS', 'Rio Grande do Sul'),
                                 ('RO', 'Rondônia'),
                                 ('RR', 'Roraima'),
                                 ('SC', 'Santa Catarina'),
                                 ('SP', 'São Paulo'),
                                 ('SE', 'Sergipe'),
                                 ('TO', 'Tocantins'),
                             ))
    zipcode = models.CharField(verbose_name='CEP', max_length=10)
    phone = models.CharField(verbose_name='telefone', max_length=13)
    email = models.CharField(verbose_name='e-mail', max_length=100)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def clean(self):
        errormsg = {}

        sendedcpf = self.cpf or None
        savedcpf = None
        profile = Profile.objects.filter(cpf=sendedcpf).first()

        if profile:
            savedcpf = profile.cpf
            if savedcpf is not None and self.pk != profile.pk:
                errormsg['cpf'] = 'CPF Já Existente!'

        # if not validatecpf(self.cpf):
        #    errormsg['cpf'] = 'CPF Inválido!'

        if re.search(r'[^0-9]', self.zipcode) or len(self.zipcode) < 8:
            errormsg['zipcode'] = 'CEP Inválido!'

        if errormsg:
            raise ValidationError(errormsg)
