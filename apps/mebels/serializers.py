from rest_framework import serializers
from .models import Product, ProductShots, Brand


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    type = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = Brand
        fields = "__all__"

    def get_type(self, obj):
        if obj.category.mebels.exists():
            return 'mebels'
        elif obj.category.stones.exists():
            return 'stones'
        elif obj.category.houses.exists():
            return 'houses'
        else:
            return None


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
    products = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = "__all__"
