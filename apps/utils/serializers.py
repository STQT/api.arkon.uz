from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    phone = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()
    email_support = serializers.CharField()
    location_url = serializers.URLField()
