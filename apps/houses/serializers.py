from rest_framework import serializers
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    logo_light_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        exclude = ("content", "phone")


class BrandRetrieveSerializer(serializers.ModelSerializer):
    logo_thumbnail = serializers.ImageField()
    image_thumbnail = serializers.ImageField()
    logo_light_thumbnail = serializers.ImageField()

    class Meta:
        model = Brand
        fields = "__all__"
