from random import randint

from rest_framework import serializers
from apps.institucional.models import *

class GenerarReciboSerializer(serializers.ModelSerializer):

    programas = serializers.ChoiceField(choices=[(programa.id_programa, programa.nombre) for programa in Programa.objects.all()])
    semestre = serializers.ChoiceField(choices=[(semestre.id_semestre, semestre.nombre) for semestre in Semestre.objects.all()])

    class Meta:
        model =  Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano','programas','semestre']

    def create(self, validated_data):
        persona =  Persona.objects.create(
            nombres = validated_data['nombres'], 
            apellidos = validated_data['apellidos'], 
            cedula_ciudadano= validated_data['cedula_ciudadano']
            )
        recibo = PagoRecibo.objects.create(
            codigo      = randint(10000000, 99999999),
            semestre    = Semestre.objects.filter(id_semestre= validated_data['semestre']).first(),
            persona     = persona
        )
        return recibo

