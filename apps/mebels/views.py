from rest_framework import generics

from .models import Product, Brand
from .serializers import ProductSerializer, BrandRetrieveSerializer, BrandSerializer


class ProductAPIRetrieveView(generics.RetrieveAPIView): # noqa
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandRetrieveSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
