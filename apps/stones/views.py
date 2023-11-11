from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics

from apps.stones.models import Product, Brand, Category, Characteristic
from apps.stones.serializers import ProductSerializer, BrandRetrieveSerializer, BrandSerializer, \
    CategoryRetrieveSerializer


class ProductAPIRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandRetrieveSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryRetrieveSerializer


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
