from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('generar_recibo/', GenerarRecibo.as_view(), name= 'generar_recibo'),
    path('recibo/<id>/', Recibo.as_view(), name= 'recibo'),
    path('datos_crear_usuario/', DatosCrearUsuario.as_view(), name='datos_crear_usuario'),
    path('usuario_creado/<usuario>/<passusuario>', UsuarioNuevo.as_view(), name='usuario_creado'),
    path('matricular_asignaturas/', MatricularAsignatura.as_view(), name= 'matricular_asignaturas'),
    path('elegir_horario/<asignatura>/', ElegirHorarioEstudiante.as_view(), name= 'elegir_horario'),
    path('revisar_notas/', RevisarNotas.as_view(), name= 'revisar_notas'),
    path('elegir_horario_docente/', ElegirHorarioDocente.as_view(), name= 'elegir_horario_docente'),
    path('editar_notas/<horario>/', EditarNotas.as_view(), name= 'editar_notas'),
    path('editar_usuario/<int:pk>/', EditarUsuario.as_view(), name= 'editar_usuario'),
    path('horario_asignaturas/', HorarioAsignaturas.as_view(), name= 'horario_asignaturas'),
    path('horario_estudiantes_matriculados', HorarioEstudiantesMatriculados.as_view(), name= 'horario_estudiantes_matriculados'),
    path('estudiantes_matriculados/<horario_estudiantes>', EstudiantesMatriculados.as_view(), name= 'estudiantes_matriculados')
]
