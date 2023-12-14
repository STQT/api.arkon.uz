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
    filtered_products = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = "__all__"

    def get_filtered_products(self, obj):
        products = obj.products.filter(hide=False)
        return ProductListSerializer(products, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"


class BrandRetrieveSerializer(serializers.ModelSerializer):
    filtered_categories = serializers.SerializerMethodField()
    filtered_products = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = "__all__"

    def get_filtered_categories(self, obj):
        categories = obj.categories.filter(hide=False)
        return CategoriesSerializer(categories, many=True).data

    def get_filtered_products(self, obj):
        products = obj.products.filter(hide=False)
        return ProductListSerializer(products, many=True).data


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
