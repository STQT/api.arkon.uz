from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.stones.views import ProductAPIRetrieveView, BrandListAPIView, BrandRetrieveAPIView, CategoryRetrieveAPIView
from apps.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("stones/product/<int:pk>/", ProductAPIRetrieveView.as_view()),
    path("stones/brand-list/", BrandListAPIView.as_view()),
    path("stones/brand/<int:pk>/", BrandRetrieveAPIView.as_view()),
    path("stones/category/<int:pk>/", CategoryRetrieveAPIView.as_view()),
]
