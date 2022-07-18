import json

from django.core.exceptions import ValidationError
from django.core.serializers import serialize

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.institucional.api.serializers import *
from apps.institucional.models import *
from apps.institucional.api.funciones_serializer import *
from apps.usuario.models import *

class TramitesFuncionarioViewSet(viewsets.ViewSet):
    model = AsignaturaUsuario
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='')
    def generar_recibo_estudiante_nuevo(self, request, pk=None):
        serializer = GenerarReciboEstudianteNuevoSerializer(data=request.data)
        if serializer.is_valid():
            informacion_recibo = serializer.save()            
            return Response(informacion_recibo, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Semestre creado con esos datos'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='')
    def recibo_estudiante_nuevo(self, request, pk=None):
        recibo = PagoRecibo.objects.filter(codigo=self.kwargs['pk']).first()
        if recibo:
            datos_recibo = DatosReciboCreadoSerializer(recibo)
            return Response(datos_recibo.data, status=status.HTTP_200_OK)
        return Response({'error':'La información dada para recibo no es válida'},status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='')
    def recibo_estudiante_antiguo(self, request, pk=None):
        persona = Persona.objects.filter(id=self.kwargs['pk']).first()
        if usuario:
            recibo = recibo_por_pagar_estudiante_antiguo(
                persona.id,
                persona.semestre.id
            )
            return Response(recibo, status=status.HTTP_201_CREATED)
        return Response({'error': 'Los datos suministrados para la persona son incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)
            
        
    @action(methods=['post'], detail=False, url_path='')
    def crear_usuario_estudiante(self, request, pk=None):
        serializer = CrearUsuarioEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            usuario_creado = serializer.save()
            return Response(usuario_creado, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=False, url_path='')
    def usuarios_antiguos_para_matricuar(self, request, pk=None):
        estudiantes_activos = Usuario.objects.filter(is_active=True, rol__nombre="Estudiante")
        if estudiantes_activos:
            datos_estudiantes = DatosEstudiantesMatricularSerializer(estudiantes_activos)
            return Response(usuario_creado, status=status.HTTP_200_OK)
        return Response({'error': 'No se encontraron estudiantes activos.'},status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=True, url_path='')
    def usuario_creado(self, request, pk=None):
        usuario = Usuario.objects.filter(id=self.kwargs['pk']).first()
        if usuario:
            datos_usuario = DatosUsuarioNuevoSerializer(usuario)
            return Response(datos_usuario.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'La clave otorgada para un usuario es invalida.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='')
    def matricular_asignatura_estudiante(self, request, pk=None):
        if AsignaturaUsuario.objects.filter(usuario=request.user, activo=True).exists():
            query_asignaturas = obtener_asignaturas_matriculables(request.user)
            serializer = DetalleAsignaturaUsuarioSerializer(query_asignaturas)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen asignaturas activas para este usuario'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='')
    def agregar_notas_a_estudiante(self, request, pk=None):
        if HorarioAsignatura.objects.filter(docente=request.user).exists():
            pass
        else:
            return Response({'error': 'No existen horarios asignados para este usuario'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='')
    def plantilla_inicio(self, request, pk=None):
        return Response({'mensaje': 'Se ha iniciado sesion satisfactoriamente.'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='')
    def obtener_horarios_asignatura(self, request, pk=None):
        asignatura_usuario = AsignaturaUsuario.objects.filter(id=self.kwargs['pk']).first()
        if asignatura_usuario:
            serializer = ObtenerHorariosSerializer(asignatura_usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen horarios asociados para esta asigntura'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='')
    def matricular_horario(self, request, pk=None):
        asignatura_usuario = AsignaturaUsuario.objects.filter(id=self.kwargs['id']).first()
        if asignatura_usuario:
            pass

    @action(methods=['get'], detail=False, url_path='')
    def agregar_notas_estudiante(self, request, pk=None):
        horarios_docente = HorarioAsignatura.objects.filter(docente=request.user)
        if horarios_docente:
            serializer = EstudiantesMatriculadosSerializer(horarios_docente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen estudiantes matriculados con el docente'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='')
    def agregar_nota_corte(self, request, pk=None):
        asignatura_usuario = AsignaturaUsuario.objects.filter(id=self.kwargs['pk']).first()
        if asignatura_usuario:
            serializer = AgregarNotaCorteSerializer(asignatura_usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen un usuario asociado a la asignatura con dichas credenciales.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='')
    def simulador_pago_recibo(self, request, pk=None):
        serializer = SimuladorPagoReciboRestSerializer(data=request.data)
        if serializer.is_valid():
            informacion_pago = serializer.save()            
            return Response(informacion_pago, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
