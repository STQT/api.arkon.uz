from rest_framework import serializers
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    type = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = Brand
        exclude = ("content", "phone")

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
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"
