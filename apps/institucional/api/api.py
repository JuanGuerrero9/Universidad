from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.institucional.api.serializers import *
from apps.institucional.models import *


# TRABAJAR CON VIEWSETS

# - CREATEAPIVIEW -

class GenerarReciboEstudianteNuevoCreateAPIView(generics.CreateAPIView):

    serializer_class = GenerarReciboEstudianteNuevoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "id_programa": self.kwargs['pk']
            }
        )
        return context
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recibo = serializer.save()
            return Response({
                'Mensaje':f'''El recibo se ha creado sactisfactoriamente con el codigo {recibo.codigo}, 
                            vinculado a la persona {recibo.persona.nombres} {recibo.persona.apellidos}'''
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class GenerarReciboEstudianteAntiguoCreateAPIView(generics.CreateAPIView):

    serializer_class = GenerarReciboEstudianteAntiguoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recibo = serializer.save()
            if recibo is not None:
                return Response({
                    'mensaje':f'''El recibo se ha creado sactisfactoriamente con el codigo {recibo.codigo}, 
                                vinculado a la persona {recibo.persona.nombres} {recibo.persona.apellidos}'''
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'El usuario no aprobó mayoria de créditos del semestre anterior.'
                }, status=status.HTTP_206_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors)



class CrearUsuarioEstudianteCreateAPIView(generics.CreateAPIView):

    serializer_class = CrearUsuarioEstudianteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({'Mensaje': f'Se ha creado exitosamente el usuario, Con Username: {usuario[0].username} y Password: {usuario[1]}'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class SimuladorPagoReciboCreateAPIView(generics.CreateAPIView):

    serializer_class = SimuladorPagoReciboSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "usuario": self.request.user
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tarjeta = serializer.save()
            if tarjeta is not None:
                return Response({'Mensaje': 'Se ha realizado la transaccion de pago de semestre sactisfactoriamente.'}
            , status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'La tarjeta asignada no tiene los saldos suficientes.'
                }, status=status.HTTP_206_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors)
            


class AsignarHorarioAsignaturaCreateAPIView(generics.CreateAPIView):

    serializer_class = EleccionHorarioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            asignatura = serializer.save(self.kwargs['pk'])
            return Response({'Mensaje': f'La asignatura {asignatura.asignatura} se le ha añadido correctamente el horario'}
            , status=status.HTTP_201_CREATED)

class EleccionTipoEstudiantePorMatricularCreateAPIView(generics.CreateAPIView):

    serializer_class = EleccionTipoEstudiantePorMatricularSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo_estudiante = serializer.save()
            if tipo_estudiante == 'ESTUDIANTE_NUEVO':
                id_programa = self.kwargs['pk']
                return redirect(f'/rest/institucional/generar_recibo_estudiante_nuevo/{id_programa}/')
            elif tipo_estudiante == 'ESTUDIANTE_ANTIGUO':
                return redirect(f'/rest/institucional/generar_recibo_estudiante_antiguo/')
        else:
            return Response(serializer.errors)

class EleccionTipoUsuarioCreateAPIView(generics.CreateAPIView):

    serializer_class = EleccionTipoUsuarioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo_usuario = serializer.save()
            if tipo_usuario == 'DOCENTE':
                return redirect(f'/rest/institucional/generar_recibo_usuario_nuevo/{id_programa}/')
            elif tipo_usuario == 'ESTUDIANTE':
                return redirect(f'/rest/institucional/crear_usuario_estudiante/')
        else:
            return Response(serializer.errors)


class EleccionProgramaGenerarReciboCreateAPIView(generics.CreateAPIView):

    serializer_class = EleccionProgramaGenerarReciboSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            programa = serializer.save()
            return redirect(f'/rest/institucional/elegir_estudiante_por_matricular/{programa.id}/')
        else:
            return Response(serializer.errors)

class AsignarNotaCorteCreateAPIView(generics.CreateAPIView):

    serializer_class = AsignarNotaAsignaturaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            asignatura_usuario = serializer.save()
            return Response({'Mensaje': 'Se ha asignado sactisfactoriamente el horario a la asignatura escogida'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.erros)




# - LISTCREATEAPIVIEW -

class EleccionAsignaturaAsignarNotaCorteListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = EleccionAsignaturaAsignarNotaCorteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'usuario': self.request.user
            }
        )

    def list(self, request, *args, **kwargs):
        queryset = obtener_asignaturas_activas(self.request.user)
        serializer = EleccionAsignaturaAsignarNotaCorteSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            asignatura_usuario = serializer.save()
            return redirect(f'/rest/institucional/asignar_nota_corte/{asignatura_usuario.id}/')
        else:
            return Response(serializer.errors)


class EleccionAsignaturaPorMatricularListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]

    serializer_class = EleccionAsignaturaPorMatricularSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "id_usuario": self.request.user
            }
        )
        return context

    def list(self, request, *args, **kwargs):
        queryset = obtener_asignaturas_matriculables(request.user)
        serializer = EleccionAsignaturaPorMatricularSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            asignatura_usuario = serializer.save()
            return redirect(f'/rest/institucional/asignar_horario_asignatura/{asignatura_usuario}/')
        else:
            return Response(serializer.errors)

class AsignarHorarioAsignaturaListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]

    serializer_class = EleccionHorarioSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "id_asignatura_usuario": self.kwargs['pk']
            }
        )
        return context

    def list(self, request, *args, **kwargs):
        asignatura = Asignatura.objects.filter(id=self.kwargs['pk']).values_list('id', flat=True).first()
        queryset = obtener_horario_asignatura(asignatura)
        serializer = EleccionHorarioSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Mensaje': 'Se ha añadido sactisfactoriamente el horario a tu asignatura.'}
            , status=status.HTTP_201_CREATEqD)
        else:
            return Response(serializer.errors)


