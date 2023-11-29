from rest_framework import serializers

from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = Category
        fields = "__all__"

    def get_type(self, obj):
        if obj.mebels.exists():
            return 'mebels'
        elif obj.stones.exists():
            return 'stones'
        elif obj.houses.exists():
            return 'houses'
        else:
            return None
