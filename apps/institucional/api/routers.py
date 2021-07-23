from django.urls import path

from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.institucional.api.api import *


router= routers.DefaultRouter()

urlpatterns = [ 
    path('generar_recibo/', GenerarReciboCreateAPIView.as_view(), name="generar_recibo"),
]

urlpatterns += router.urls
