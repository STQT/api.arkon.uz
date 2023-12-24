from rest_framework import serializers
from .models import Product, Characteristic, Brand, Categories, ProductShots, BrandSocials, BrandLocations
from ..categories.models import Table
from ..utils.serializers import AddressSerializer


class BrandSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandSocials
        fields = ("link", "type")


class BrandLocationsSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(source="brand.icon")
    name = serializers.CharField(source="brand.name")

    class Meta:
        model = BrandLocations
        exclude = ("id",)


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
    brand_data = AddressSerializer(source="brand")
    socials = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = "__all__"

    def get_socials(self, obj):
        return BrandSocialsSerializer(obj.brand.socials, context=self.context, many=True).data

    def get_filtered_products(self, obj):
        products = obj.products.filter(hide=False)
        return ProductListSerializer(products, context=self.context, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    socials = BrandSocialsSerializer(many=True)

    class Meta:
        model = Brand
        exclude = ("created_at", "updated_at", "hide", "phone")


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
        fields = ['name', 'value', 'type']


class ProductShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShots
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    brand_data = serializers.SerializerMethodField()
    shots = ProductShotsSerializer(many=True)
    socials = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_brand_data(self, obj):
        if obj.brand:
            return AddressSerializer(obj.brand, context=self.context, many=False).data
        elif obj.category:
            return AddressSerializer(obj.category.brand, context=self.context, many=False).data
        return None

    def get_socials(self, obj):
        if obj.brand:
            return BrandSocialsSerializer(obj.brand.socials, context=self.context, many=True).data
        elif obj.category:
            return BrandSocialsSerializer(obj.category.brand.socials, context=self.context, many=True).data
        return None

    def get_characteristics(self, obj):
        characteristics_data = obj.characteristics.all()

        characteristics_by_table = {}

        for characteristic in characteristics_data:
            table_name = characteristic.type.name
            if table_name not in characteristics_by_table:
                characteristics_by_table[table_name] = {"table_name": table_name,
                                                        "is_show": characteristic.type.is_show,
                                                        "data": []}

            characteristics_by_table[table_name]["data"].append(CharacteristicSerializer(characteristic).data)

        non_empty_tables = [data for data in characteristics_by_table.values() if data["data"]]

        return non_empty_tables
