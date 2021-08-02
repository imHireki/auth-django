"""
Core URL configuration

The `urlpatterns` list routes URLs to views
"""

# Django
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.urls')),
]
