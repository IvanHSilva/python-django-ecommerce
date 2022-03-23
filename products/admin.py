from django.contrib import admin
from .models import Product, ProdVariation


class ProdVariationInLine(admin.TabularInline):
    model = ProdVariation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'getprice', 'type']
    inlines = [ProdVariationInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProdVariation)
