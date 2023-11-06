from django.contrib import admin
from .models import Product, Characteristic, Brand, Category


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [CharacteristicInline]
    list_display = ('name', 'image', 'arkon_url')
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
class BrandAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
