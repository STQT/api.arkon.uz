from rest_framework import serializers
from .models import Product, ProductShots, Brand


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    logo_light_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"

class ProductShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShots
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    shots = ProductShotsSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class BrandRetrieveSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    logo_light_thumbnail = serializers.ImageField()
    products = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = "__all__"
