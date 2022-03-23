from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(
        User, verbose_name='usuário', on_delete=models.DO_NOTHING)
    total = models.FloatField(verbose_name='total')
    status = models.CharField(default='A', max_length=1, verbose_name='status',
                              choices=(
                                  ('E', 'Em Análise'),
                                  ('A', 'Aprovado'),
                                  ('R', 'Reprovado'),
                                  ('P', 'Pendente'),
                                  ('E', 'Enviado'),
                                  ('F', 'Finalizado'),
                              ))

    def __str__(self) -> str:
        return f'Pedido nº {self.pk}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name='pedido', on_delete=models.CASCADE)
    product = models.CharField(max_length=100, verbose_name='produto')
    productid = models.PositiveIntegerField(verbose_name='id produto')
    variation = models.CharField(max_length=100, verbose_name='variação')
    variationid = models.PositiveIntegerField(verbose_name='id variação')
    price = models.FloatField(verbose_name='preço')
    promoprice = models.FloatField(default=0, verbose_name='promocional')
    quantity = models.PositiveIntegerField(verbose_name='quantidade')
    image = models.CharField(max_length=500, verbose_name='imagem')

    def __str__(self) -> str:
        return f'Item do Pedido {self.pk}'

    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedidos'
