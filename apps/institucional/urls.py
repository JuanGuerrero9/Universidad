from django.urls import path, re_path
from .views import *

urlpatterns = [
    # URL FUNCIONARIO
    path('generar_recibo/', GenerarRecibo.as_view(), name='generar_recibo'),
    path('recibo/', Recibo.as_view(), name='recibo'),
    path('crear_usuario_estudiante/', CrearUsuarioEstudianteView.as_view(), name='crear_usuario_estudiante'),
    path('crear_usuario_docente/', CrearUsuarioDocenteView.as_view(), name='crear_usuario_docente'),
    path('usuario_creado/', UsuarioNuevo.as_view(), name='usuario_creado'),
    path('estudiante_nuevo/<int:pk>/', MatricularEstudianteNuevoView.as_view(), name='estudiante_nuevo'),
    path('estudiante_antiguo/<int:pk>/', MatricularEstudianteAntiguoView.as_view(), name='estudiante_antiguo'),
    path('simulador_pago_recibo/', SimuladorPagoRecibo.as_view(), name='simulador_pago_recibo'),
    path('recibo_pagado/', ReciboPagado.as_view(), name='recibo_pagado'),

    # URL ESTUDIANTE
    path('matricular_asignaturas/', MatricularAsignatura.as_view(), name='matricular_asignaturas'),
    path('elegir_horario/', ElegirHorarioEstudiante.as_view(), name='elegir_horario'),
    path('revisar_notas/', RevisarNotas.as_view(), name='revisar_notas'),
    path('horario_asignaturas/', HorarioAsignaturas.as_view(), name='horario_asignaturas'),

    # URL DOCENTE
    path('editar_notas/', EditarNotas.as_view(), name='editar_notas'),
    path('actualizar_notas/', ActualizarNotas.as_view(), name='actualizar_notas'),
    path('estudiantes_matriculados/', EstudiantesMatriculados.as_view(), name='estudiantes_matriculados'),
    path('horario_docente_asignaturas', HorarioDocenteAsignaturas.as_view(), name='horario_docente_asignaturas'),

    # URL para cualquier ROL
    path('editar_usuario/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
]
