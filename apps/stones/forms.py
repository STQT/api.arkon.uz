from django import forms
from django.forms import BaseInlineFormSet

from apps.stones.models import ProductShots, Product


class ImagePreviewWidget(forms.widgets.ClearableFileInput):
    template_name = 'stones/widgets/image_preview_widget.html'  # Create a template for the widget


class ProductShotsForm(forms.ModelForm):
    image_preview = forms.ImageField(widget=ImagePreviewWidget(attrs={'readonly': True, 'disabled': True}),
                                     required=False, label="Предосмотр")

    class Meta:
        model = ProductShots
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.image:
            self.initial['image_preview'] = self.instance.image

    def save(self, commit=True):
        # Save the form and update the image field if the preview field is present
        image_preview = self.cleaned_data.get('image_preview')
        if image_preview:
            self.instance.image = image_preview
        return super().save(commit=commit)


class CustomProductShotsInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        instance = super().save_new(form, commit=False)

        # If 'image_preview' is provided, update 'image' field
        image_preview = form.cleaned_data.get('image_preview')
        if image_preview:
            instance.image = image_preview

        if commit:
            instance.save()

        return instance


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        brand = cleaned_data.get('brand')

        if category and brand:
            raise forms.ValidationError("Выберите либо Модель либо Бренд")

        if category is None and brand is None:
            raise forms.ValidationError("Вам нужно указать либо Модель либо Бренд для корректной работы")
