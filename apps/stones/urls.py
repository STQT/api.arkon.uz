from django.urls import path
from . import views

app_name = "actions"
urlpatterns = [
    path('hide/<int:pk>/<str:view_obj>/', views.hide, name='hide'),
    path('activate/<int:pk>/<str:view_obj>/', views.activate, name='activate'),
    path('clone/<int:pk>/<str:view_obj>/', views.clone, name='clone'),
    path('delete/<int:pk>/<str:view_obj>/', views.delete, name='delete'),
    path('show/<int:pk>/<str:view_obj>/', views.preview_show, name='show'),
]
