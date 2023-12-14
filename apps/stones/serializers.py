from rest_framework import serializers
from .models import Product, Characteristic, Brand, Categories
from ..utils.serializers import AddressSerializer


class ProductListSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Product
        exclude = ("arkon_file", "category")


class CategoriesSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Categories
        fields = "__all__"


class CategoriesRetrieveSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = Categories
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"


class BrandRetrieveSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True)
    products = ProductListSerializer(many=True)

    class Meta:
        model = Brand
        fields = "__all__"


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    brand_data = AddressSerializer(source="category.brand")

    class Meta:
        model = Product
        fields = "__all__"

    def get_characteristics(self, obj):
        characteristics_by_type = {
            "main": [],
            "standart": [],
            "test": []
        }

        for characteristic in obj.characteristics.all():
            type_key = characteristic.type
            if type_key not in characteristics_by_type:
                characteristics_by_type[type_key] = []

            characteristics_by_type[type_key].append(CharacteristicSerializer(characteristic).data)

        return characteristics_by_type
