from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.stones import views as stone_views
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
    path("countries/", stone_views.CountryListView.as_view()),
    path("stones/brand-list/", stone_views.BrandListAPIView.as_view()),
    path("stones/brand/<int:pk>/", stone_views.BrandRetrieveAPIView.as_view()),
    path("stones/category/<int:pk>/", stone_views.CategoriesRetrieveAPIView.as_view()),
    path("categories/", category_views.CategoryAPIListView.as_view()),
    path('all-locations/', stone_views.AllLocationsListView.as_view(), name='all-locations-list'),
]
