from django_countries import Countries
from rest_framework import serializers
from .models import Product, Characteristic, Brand, Categories, ProductShots, BrandSocials
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


class CountryListSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class CategoriesRetrieveSerializer(serializers.ModelSerializer):
    filtered_products = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = "__all__"

    def get_filtered_products(self, obj):
        products = obj.products.filter(hide=False)
        return ProductListSerializer(products, context=self.context, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        exclude = ("created_at", "updated_at", "hide", "phone")


class BrandSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandSocials
        fields = ("link", "type")


class BrandRetrieveSerializer(serializers.ModelSerializer):
    filtered_categories = serializers.SerializerMethodField()
    filtered_products = serializers.SerializerMethodField()
    socials = BrandSocialsSerializer(many=True)

    class Meta:
        model = Brand
        fields = "__all__"

    def get_filtered_categories(self, obj):
        categories = obj.categories.filter(hide=False)
        return CategoriesSerializer(categories, context=self.context, many=True).data

    def get_filtered_products(self, obj):
        products = obj.products.filter(hide=False)
        return ProductListSerializer(products, context=self.context, many=True).data


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['name', 'value']


class ProductShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShots
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    brand_data = serializers.SerializerMethodField()
    shots = ProductShotsSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_brand_data(self, obj):
        if obj.brand:
            return AddressSerializer(obj.brand, context=self.context, many=False).data
        elif obj.category:
            return AddressSerializer(obj.category.brand, context=self.context, many=False).data
        return None

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
