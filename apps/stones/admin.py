from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Product, Characteristic, Brand, Category


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [CharacteristicInline]
    list_display = ('name', 'arkon_url', 'image_preview', 'tools_column')
    actions = ['duplicate_product']
    save_as = True

    def tools_column(self, obj):
        html_tag = '<a href="{0}" class="btn btn-primary">Клонировать</a> '

        return mark_safe(
            html_tag.format(
                reverse('duplicate_stones_product', args=[obj.pk]), )
        )

    tools_column.short_description = 'Инструменты'
    tools_column.allow_tags = True

    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="200"/>'  # if obj.image else '<div>Rasmsiz</div>'
        )

    image_preview.short_description = 'Фото'
    image_preview.allow_tags = True

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
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']

    def logo_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.logo_light.url}" width="200"/>'  # if obj.logo_light else '<div>Rasmsiz</div>'
        )

    logo_preview.short_description = 'Фото'
    logo_preview.allow_tags = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview']

    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="200"/>'  # if obj.image else '<div>Rasmsiz</div>'
        )

    image_preview.short_description = 'Фото'
    image_preview.allow_tags = True
