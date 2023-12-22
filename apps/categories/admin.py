from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'order', 'hide']
    list_display_links = ['name', 'image_preview']
    list_editable = ['order']

    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="200"/>'  # if obj.image else '<div>Rasmsiz</div>'
        )

    image_preview.short_description = 'Фото'
    image_preview.allow_tags = True
