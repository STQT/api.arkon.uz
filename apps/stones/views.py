from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from django_countries.data import COUNTRIES
from django_countries.fields import Country
from rest_framework.response import Response

from apps.stones.models import Product, Brand, Characteristic, Categories, BrandLocations
from apps.stones.serializers import (ProductSerializer, BrandRetrieveSerializer, BrandSerializer,
                                     CategoriesRetrieveSerializer, CountryListSerializer, BrandLocationsSerializer)

from django_countries.fields import Country

modelClass = {
    "product": Product,
    "categories": Categories,
    "brand": Brand
}


def get_english_country_names(country_codes):
    english_country_names = {}
    for code in country_codes:
        english_country_names[code] = Country(code).name
    return english_country_names


class CountryListView(generics.ListAPIView):
    serializer_class = CountryListSerializer

    def get_queryset(self):
        country_codes = Brand.objects.filter(hide=False).values_list('country', flat=True).distinct()
        return country_codes

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        english_country_names = get_english_country_names(queryset)
        countries_data = [{'code': code, 'name': english_country_names[code]} for code in queryset]
        serializer = self.get_serializer(countries_data, many=True)
        return Response(serializer.data)


class ProductAPIRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('brand', 'category__brand').prefetch_related("shots", "characteristics")
    serializer_class = ProductSerializer


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandRetrieveSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.filter(hide=False).order_by('order', 'pk')
    serializer_class = BrandSerializer
    filterset_fields = {
        "category_id": ("exact",),
        "name": ("icontains",),
        "country": ("exact",)
    }


class CategoriesRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Categories.objects.select_related("brand")
    serializer_class = CategoriesRetrieveSerializer


class AllLocationsListView(generics.ListAPIView):
    queryset = BrandLocations.objects.select_related("brand")
    serializer_class = BrandLocationsSerializer


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
    url_links = {
        "product": f"/product/{pk}",
        "categories": f"/product?id={pk}",
        "brand": f"/home?id={pk}"
    }
    return redirect("https://web.arkon.uz" + url_links[view_obj])
