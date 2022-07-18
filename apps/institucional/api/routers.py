from django.urls import path
from django.contrib.auth.decorators import login_required

from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter


from .viewsets import *

from apps.institucional.api.api import *


# Corregir routers



urlpatterns = [ 
    # path('generar_recibo_estudiante_nuevo/<int:pk>/', GenerarReciboEstudianteNuevoCreateAPIView.as_view(),\
    #  name="generar_recibo_estudiante_nuevo"),
    path('generar_recibo_estudiante_antiguo/', GenerarReciboEstudianteAntiguoCreateAPIView.as_view(),\
     name="generar_recibo_estudiante_antiguo"),
    path('eleccion_asignatura_asignar_nota/', EleccionAsignaturaAsignarNotaCorteListCreateAPIView.as_view(),\
     name="eleccion_asignatura_asignar_nota"),
    path('asignar_nota_corte/<int:pk>/', AsignarNotaCorteCreateAPIView.as_view(), name="asignar_nota_corte"),
    path('eleccion_programa_recibo/', EleccionProgramaGenerarReciboCreateAPIView.as_view(), name="eleccion_programa_recibo"),
    path('eleccion_tipo_usuario/', EleccionTipoUsuarioCreateAPIView.as_view(), name="eleccion_tipo_usuario"),
    path('asignar_horario_asignatura/<int:pk>/', AsignarHorarioAsignaturaListCreateAPIView.as_view(), name="asignar_horario_asignatura"),
    path('matricular_asignatura/', EleccionAsignaturaPorMatricularListCreateAPIView.as_view(), name="matricular asignatura"),
    path('crear_usuario_estudiante/', CrearUsuarioEstudianteCreateAPIView.as_view(), name="crear_usuario_estudiante"),
    path('elegir_estudiante_por_matricular/<int:pk>/', EleccionTipoEstudiantePorMatricularCreateAPIView.as_view(),\
     name="elegir_estudiante_por_matricular"),
    path('simulador_pago_recibo/', SimuladorPagoReciboCreateAPIView.as_view(), name="simulador_pago_recibo"),
]

router= routers.DefaultRouter()

router.register(r'tramites_funcionario', TramitesFuncionarioViewSet, basename='tramites_funcionario')




urlpatterns += router.urls
