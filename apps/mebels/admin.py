from django.contrib import admin
from .models import Product, Brand, ProductShots


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductShotsInline]
    list_display = ('name', 'image', 'arkon_url')
    actions = ['duplicate_product']
    save_as = True


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    ...
