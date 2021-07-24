from django.urls import path

from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.institucional.api.api import *


router= routers.DefaultRouter()

urlpatterns = [ 
    path('generar_recibo/', GenerarReciboCreateAPIView.as_view(), name="generar_recibo"),
    path('crear_usuario/', CrearUsuarioCreateAPIView.as_view(), name="crear_usuario"),
    path('simulador_pago_recibo/', SimuladorPagoReciboCreateAPIView.as_view(), name="simulador_pago_recibo"),
]

urlpatterns += router.urls
