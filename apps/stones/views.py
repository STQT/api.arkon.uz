from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics

from apps.stones.models import Product, Brand, Characteristic, Categories
from apps.stones.serializers import ProductSerializer, BrandRetrieveSerializer, BrandSerializer, \
    CategoriesRetrieveSerializer


class ProductAPIRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('brand', 'category__brand')
    serializer_class = ProductSerializer


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandRetrieveSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.filter(hide=False)
    serializer_class = BrandSerializer
    filterset_fields = ("category_id",)


class CategoriesRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Categories.objects.select_related("brand")
    serializer_class = CategoriesRetrieveSerializer


def duplicate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    old_product_id = product.id
    product.id = None
    product.save()

    characteristics = Characteristic.objects.filter(product_id=old_product_id)
    for characteristic in characteristics:
        characteristic.id = None
        characteristic.product_id = product.id
        characteristic.save()
    return redirect(reverse('admin:stones_product_changelist'))



modelClass = {
    "product": Product,
    "categories": Categories,
    "brand": Brand
}


def clone(request, pk, view_obj):
    obj = get_object_or_404(modelClass[view_obj], id=pk)
    obj.id = None
    obj.save()
    return redirect(reverse(f'admin:stones_{view_obj}_changelist'))


def hide(request, pk, view_obj):
    obj = get_object_or_404(modelClass[view_obj], id=pk)
    obj.hide = True
    obj.save()
    return redirect(reverse(f'admin:stones_{view_obj}_changelist'))


def activate(request, pk, view_obj):
    obj = get_object_or_404(modelClass[view_obj], id=pk)
    obj.hide = False
    obj.save()
    return redirect(reverse(f'admin:stones_{view_obj}_changelist'))


def delete(request, pk, view_obj):
    obj = get_object_or_404(modelClass[view_obj], id=pk)
    obj.delete()
    return redirect(reverse(f'admin:stones_{view_obj}_changelist'))


def preview_show(request, pk, view_obj):
    obj = get_object_or_404(modelClass[view_obj], id=pk)
    obj.delete()
    return redirect(reverse(f'admin:stones_{view_obj}_changelist'))
