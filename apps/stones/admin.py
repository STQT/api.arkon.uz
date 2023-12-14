from django import forms

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .forms import ProductShotsForm, CustomProductShotsInlineFormSet, ProductAdminForm
from .models import Product, Characteristic, Brand, Categories, ProductShots
from ..utils.admin import BaseAdmin


## FORMS
class BrandAdminForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    form = ProductShotsForm
    formset = CustomProductShotsInlineFormSet
    extra = 1


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    inlines = [CharacteristicInline, ProductShotsInline]
    form = ProductAdminForm
    list_display = ('name', 'image_preview', 'category', 'brand', 'tools_column')
    list_filter = ['brand', 'category']
    list_display_links = ["name", "image_preview", "category", "brand"]
    search_fields = ['name', 'brand__name', 'category__name']
    actions = ['duplicate_product']
    save_as = True

    def duplicate_product(self, request, queryset):
        for product in queryset:
            old_product_id = product.id
            product.id = None
            product.save()

            characteristics = Characteristic.objects.filter(product_id=old_product_id)
            for characteristic in characteristics:
                characteristic.id = None
                characteristic.product_id = product.id
                characteristic.save()

        self.message_user(request, "Выбранные продукты были успешно дублированы")

    duplicate_product.short_description = "Дублировать данные продукты"


@admin.register(Brand)
class BrandAdmin(BaseAdmin):
    list_display = ['name', 'category', 'logo_preview', 'image_preview', 'tools_column']
    list_filter = ['category']
    list_display_links = ['name', 'logo_preview', 'category']
    search_fields = ['name', 'category__name']
    form = BrandAdminForm

    def logo_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.logo.url}" width="200"/>'  # if obj.logo_light else '<div>Rasmsiz</div>'
        )

    logo_preview.short_description = 'Логотип'
    logo_preview.allow_tags = True


@admin.register(Categories)
class CategoriesAdmin(BaseAdmin):
    list_display = ['name', 'brand', 'image_preview', 'tools_column']
    list_display_links = ['name', 'image_preview', 'tools_column']
    search_fields = ['name', 'brand__name']
    list_filter = ['brand']
