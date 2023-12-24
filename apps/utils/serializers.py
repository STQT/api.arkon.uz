from rest_framework import serializers

from apps.stones.models import Brand


class AddressSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()
    email_support = serializers.CharField()
    location_url = serializers.URLField()
    information_label = serializers.CharField()

    class Meta:
        model = Brand
        fields = ("phone", "address", "email", "email_support", "location_url", "information_label")
