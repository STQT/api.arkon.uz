from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import ProductShotsForm, ProductAdminForm, CustomProductShotsInlineFormSet
from .models import Product, Brand, ProductShots


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductShotsInline]
    form = ProductAdminForm
    fieldsets = [
        ('Основные информации продукта', {
            'fields': ['brand', 'name', 'arkon_url', 'is_album'],
        }),
        ('Изображение в главном меню', {
            'fields': ['image', 'image_preview'],
            'classes': ['wide', 'extrapretty'],
        }),
        ('Дополнительные изображения для главного меню', {
            'fields': ['image2', 'image_preview2', 'image3', 'image_preview3'],
            'classes': ['wide', 'extrapretty'],
        }),
    ]
    list_display = ('name', 'arkon_url', 'image_preview')

    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="200"/>'  # if obj.logo_light else '<div>Rasmsiz</div>'
        )

    image_preview.short_description = 'Фото на списочном выводе'
    image_preview.allow_tags = True


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'category']
    form = BrandAdminForm

    def logo_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.logo.url}" width="200"/>'  # if obj.logo_light else '<div>Rasmsiz</div>'
        )

    logo_preview.short_description = 'Фото'
    logo_preview.allow_tags = True
