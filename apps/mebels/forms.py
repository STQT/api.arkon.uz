from django import forms
from django.forms import BaseInlineFormSet
from django.utils.safestring import mark_safe

from apps.mebels.models import ProductShots
from apps.stones.models import Product


class ImagePreviewWidget(forms.widgets.ClearableFileInput):
    template_name = 'mebels/widgets/image_preview_widget.html'  # Create a template for the widget


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


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    image_preview = forms.ImageField(widget=ImagePreviewWidget(attrs={'readonly': True, 'disabled': True}),
                                     required=False, label="Предосмотр")
    image_preview2 = forms.ImageField(widget=ImagePreviewWidget(attrs={'readonly': True, 'disabled': True}),
                                      required=False, label="Предосмотр")
    image_preview3 = forms.ImageField(widget=ImagePreviewWidget(attrs={'readonly': True, 'disabled': True}),
                                      required=False, label="Предосмотр")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the label of the original 'image' field as safe
        self.fields['image'].label = mark_safe(self.fields['image'].label)

        # If there's an existing instance with an image, set the initial value for the preview field
        if self.instance and self.instance.image:
            self.initial['image_preview'] = self.instance.image
            self.initial['image_preview2'] = self.instance.image2
            self.initial['image_preview3'] = self.instance.image3



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
