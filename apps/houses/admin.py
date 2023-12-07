from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Brand


class BrandAdminForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True


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
