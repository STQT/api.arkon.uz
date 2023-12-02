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

    def get_type(self, obj):
        if obj.category.mebels.exists():
            return 'mebels'
        elif obj.category.stones.exists():
            return 'stones'
        elif obj.category.houses.exists():
            return 'houses'
        else:
            return None


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
    characteristics = serializers.SerializerMethodField()

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
