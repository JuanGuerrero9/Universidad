from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from apps.institucional.api.serializers import GenerarReciboSerializer
from apps.institucional.models import *


class GenerarReciboCreateAPIView(generics.CreateAPIView):

    serializer_class = GenerarReciboSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            recibo = serializer.save()
            return Response({'Mensaje':f'El recibo se ha creado sactisfactoriamente con el codigo {recibo.codigo}, vinculado a la persona {recibo.persona.nombres} {recibo.persona.apellidos}'})


class CrearUsuarioCreateAPIView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        pass
