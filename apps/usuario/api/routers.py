from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.usuario.api.api import  UsuarioViewSet


router= DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')

urlpatterns= [
    
]

urlpatterns += router.urls
