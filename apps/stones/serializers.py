from rest_framework import serializers
from .models import Product, Characteristic, Category, Brand


class ProductListSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Product
        exclude = ("arkon_url", "category")


class CategorySerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Category
        fields = "__all__"


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"


class BrandRetrieveSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Brand
        fields = "__all__"


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    characteristics = CharacteristicSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        grouped_characteristics = {}
        for characteristic in data['characteristics']:
            type_key = characteristic['name']
            if type_key not in grouped_characteristics:
                grouped_characteristics[type_key] = []
            grouped_characteristics[type_key].append(characteristic)
        data['grouped_characteristics'] = grouped_characteristics
        return data
