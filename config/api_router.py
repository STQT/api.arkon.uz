from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.stones import views as stone_views
from apps.mebels import views as mebel_views
from apps.houses import views as house_views
from apps.categories import views as category_views
from apps.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("stones/product/<int:pk>/", stone_views.ProductAPIRetrieveView.as_view()),
    path("stones/brand-list/", stone_views.BrandListAPIView.as_view()),
    path("stones/brand/<int:pk>/", stone_views.BrandRetrieveAPIView.as_view()),
    path("stones/category/<int:pk>/", stone_views.CategoryRetrieveAPIView.as_view()),
    path("mebels/product/<int:pk>/", mebel_views.ProductAPIRetrieveView.as_view()),
    path("mebels/brand-list/", mebel_views.BrandListAPIView.as_view()),
    path("mebels/brand/<int:pk>/", mebel_views.BrandRetrieveAPIView.as_view()),
    path("houses/brand-list/", house_views.BrandListAPIView.as_view()),
    path("houses/brand/<int:pk>/", house_views.BrandRetrieveAPIView.as_view()),
    path("categories/", category_views.CategoryAPIListView.as_view()),
]
