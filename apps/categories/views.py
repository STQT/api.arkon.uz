from rest_framework.generics import ListAPIView

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class CategoryAPIListView(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = CategorySerializer
