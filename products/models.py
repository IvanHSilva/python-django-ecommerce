import imp
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from utils import utils
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    description = models.TextField(max_length=255, verbose_name='descrição')
    image = models.ImageField(
        upload_to='prodimages/%Y/%m', blank=True, null=True, verbose_name='imagem')
    slug = models.SlugField(unique=True, blank=True,
                            null=True, verbose_name='slug')
    price = models.FloatField(verbose_name='preço')
    promoprice = models.FloatField(default=0, verbose_name='promocional')
    type = models.CharField(default='D', max_length=1, verbose_name='tipo',
                            choices=(
                                ('P', 'Padrão'), ('V', 'Variação'),
                            ))

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def getprice(self):
        return utils.formatprice(self.price)
    getprice.short_description = 'Preço'

    @staticmethod
    def imgresize(img, newwidth=800):
        imgpath = settings.MEDIA_ROOT / img
        img = Image.open(imgpath)
        width, height = img.size
        # print(f'Tamanho original: {width} X {height}')
        newheight = round((newwidth * height) / width)
        # print(f'Novo tamanho: {newwidth} X {newheight}')

        if width > newwidth:
            newimg = img.resize((newwidth, newheight), Image.ANTIALIAS)
            newimg.save(imgpath, optimize=True, quality=75)
            newimg.close()

    def saveimg(self, *args, **kwargs):

        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug
            print(slug)
            print('sem slug')

        super().save(*args, **kwargs)

        maxsize = 800

        if self.image:
            self.imgresize(self.image, maxsize)

    def __str__(self) -> str:
        return self.name


class ProdVariation(models.Model):
    product = models.ForeignKey(
        Product, verbose_name='produto', on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100, verbose_name='nome', blank=True, null=True)
    price = models.FloatField(verbose_name='preço')
    promoprice = models.FloatField(default=0, verbose_name='promocional')
    stock = models.PositiveIntegerField(default=1, verbose_name='estoque')

    def __str__(self):
        return self.name or self.product.name

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
