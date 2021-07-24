from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from apps.institucional.api.serializers import GenerarReciboSerializer, CrearUsuarioSerializer, SimuladorPagoReciboSerializer
from apps.institucional.models import *


class GenerarReciboCreateAPIView(generics.CreateAPIView):

    serializer_class = GenerarReciboSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            recibo = serializer.save()
            return Response({'Mensaje':f'El recibo se ha creado sactisfactoriamente con el codigo {recibo.codigo}, vinculado a la persona {recibo.persona.nombres} {recibo.persona.apellidos}'})


class CrearUsuarioCreateAPIView(generics.CreateAPIView):

    serializer_class = CrearUsuarioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({'Mensaje': f'Se ha creado exitosamente el usuario, Con Username: {usuario[0].username} y Password: {usuario[1]}'})


class SimuladorPagoReciboCreateAPIView(generics.CreateAPIView):

    serializer_class = SimuladorPagoReciboSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            tarjeta = serializer.save()
            return Response({'Mensaje': 'Se ha pagado exitosamente el recibo con el numero # , quedando el siguiente saldo en su tarjeta'})
