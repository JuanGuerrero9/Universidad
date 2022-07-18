from random import randint
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.serializers import serialize


from apps.institucional.models import *
from apps.usuario.models import *
from .funciones_serializer import *


class DetallePersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano','id']

class DatosEstudiantesMatricularSerializer(serializers.ModelSerializer):

    persona = DetallePersonaSerializer(many=True)
    
    class Meta:
        model = Usuario
        fields = ('persona',)
        depth = 2
    
    def to_representation(self, instance):
        lista = []
        for usuario in instance:
            dicty = {}
            dicty['nombre_completo'] = f'{instance.persona.nombres} {instance.persona.apellidos}'
            dicty['cedula_ciudadano'] = instance.persona.cedula_ciudadano
            dicty['id_persona'] = instance.persona.id
            lista.append(dicty)
        return lista

class SimuladorPagoReciboRestSerializer(serializers.ModelSerializer):
    codigo_recibo = serializers.IntegerField()
    class Meta:
        model = TarjetaCredito
        fields = ['numero_tarjeta', 'banco', 'codigo_seguridad', 'propietario', 'codigo_recibo']

    def validate_banco(self, value):
        if Bancos.objects.filter(id=value.id).exists():
            return value
        else:
            raise ValidationError('No existen bancos con las siguientes credenciales.')

    def validate_codigo_recibo(self, value):
        recibo = PagoRecibo.objects.filter(codigo=value).first()
        if recibo:
            if recibo.esta_pago == False:
                return value
            else:
                raise ValidationError('El recibo ya se encuentra pago.')
        else:
            raise ValidationError('No existe un recibo con los datos suministrados.')

    def validate(self, data):
        tarjeta_credito = TarjetaCredito.objects.filter(
            numero_tarjeta=data['numero_tarjeta'],
            codigo_seguridad=data['codigo_seguridad'],
            banco=data['banco'],
            propietario__iexact=data['propietario'],
        ).first()
        if tarjeta_credito:
            saldo_total = int(tarjeta_credito.saldo) + int(tarjeta_credito.credito_maximo)
            if saldo_total >= int(data['codigo_recibo']):
                return data
            else:
                raise ValidationError('La tarjeta ingresada no tiene saldo suficiente para pagar.')
        else:
            raise ValidationError('No existe una tarjeta con los datos suministrados.')

    def create(self, validated_data):
        tarjeta_credito = TarjetaCredito.objects.filter(
            numero_tarjeta=validated_data['numero_tarjeta'],
            codigo_seguridad=validated_data['codigo_seguridad'],
            propietario__iexact=validated_data['propietario'],
        ).first()
        recibo = PagoRecibo.objects.filter(codigo=validated_data['codigo_recibo']).first()
        tarjeta_credito.saldo = tarjeta_credito.saldo - recibo.semestre.costo
        tarjeta_credito.save()
        recibo.esta_pago = True
        recibo.save()
        return {
            'codigo_recibo': validated_data['codigo_recibo'],
            'valor_recibo': recibo.semestre.costo,
            'numero_tarjeta': validated_data['numero_tarjeta'],
            'saldo_tarjeta': tarjeta_credito.saldo
        }


class DatosUsuarioNuevoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        
    def to_representation(self, instance):
        return {
            'usuario': instance.username,
            'persona': f'{instance.persona.nombres} {instance.persona.apellidos}'
        }

class DatosReciboCreadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoRecibo

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'persona': f'{instance.persona.nombres} {instance.persona.apellidos}',
            'precio': instance.semestre.costo,
            'cantidad': 1
        }

class DetalleAsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ('nombre',)


class DetalleAsignaturaUsuarioSerializer(serializers.ModelSerializer):

    asignatura = DetalleAsignaturaSerializer(many=True)

    class Meta:
        model = AsignaturaUsuario
        fields = ('id', 'asignatura', 'aprobado')
        depth = 2

    def to_representation(self, instance):
        lista = []
        for asignatura in instance:
            dicty = {}
            dicty['id']= asignatura.id
            dicty['asignatura']= asignatura.asignatura.nombre
            dicty['aprobado'] = asignatura.aprobado
            lista.append(dicty)
        data = {
            'asignaturas': lista
        }
        return data

class ObtenerHorariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaUsuario
        fields = ('asignatura', 'usuario',)

    def to_representation(self, instance):
        lista = []
        horarios = HorarioAsignatura.objects.filter(asignatura=instance.asignatura)
        if horarios:
            for horario in horarios:
                dicty = {}
                dicty['docente']= f'{horario.docente.persona.nombres} {horario.docente.persona.apellidos}'
                dicty['hora_inicio'] = horario.hora_inicio
                dicty['hora_final'] = horario.hora_final
                dicty['id_horario']= horario.id
                lista.append(dicty)
        data = {
            'horarios': lista
        }
        return data

class EstudiantesMatriculadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAsignatura
        fields = ('id',)

    def to_representation(self, instance):
        lista = []
        for horario in instance:
            estudiantes = AsignaturaUsuario.objects.filter(horario_asignatura=horario.id)
            if estudiantes:
                for estudiante in estudiantes:
                    dicty = {}
                    dicty['id'] = estudiante.id
                    dicty['asignatura'] = estudiante.asignatura.nombre
                    dicty['codigo'] = estudiante.usuario.persona.codigo_universitario
                    dicty['estudiante'] = f'{estudiante.usuario.persona.nombres} {estudiante.usuario.persona.apellidos}'
                    dicty['nota_corte_1'] = estudiante.nota_corte1
                    dicty['nota_corte_2'] = estudiante.nota_corte2
                    dicty['nota_corte_3'] = estudiante.nota_corte3
                    dicty['nota_final'] = estudiante.nota_final
                    lista.append(dicty)
        data = {
            'estudiantes': lista
        }
        return data

class AgregarNotaCorteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaUsuario
        fields = ['']

    def to_representation(self, instance):
        return {
            'nota1_agregada': instance.nota1_agregada,
            'nota2_agregada': instance.nota2_agregada,
            'nota3_agregada': instance.nota3_agregada
        }

class GenerarReciboEstudianteNuevoSerializer(serializers.ModelSerializer):
    semestre = serializers.IntegerField()

    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano', 'semestre']

    def validate_semestre(self, value):
        if Semestre.objects.filter(id=value).exists():
            return value
        raise ValidationError('El semestre suministrado no existe')

    def create(self, validated_data):
        persona = crear_persona(validated_data['nombres'], validated_data['apellidos'], validated_data['cedula_ciudadano'])
        recibo = recibo_por_pagar_nuevo_estudiante(persona, validated_data['semestre'])
        return {
            'codigo': recibo.codigo,
            'persona': f'{recibo.persona.nombres} {recibo.persona.apellidos}'
            
        }


class GenerarReciboEstudianteAntiguoSerializer(serializers.Serializer):
    
    persona_para_matricular = serializers.IntegerField()

    def validate_persona_para_matricular(self, value):
        if Persona.objects.filter(id=value).exists():
            return value
        else:
            raise ValidationError('La persona enviada no existe.')

    def create(self, validated_data):
        usuario = Usuario.objects.filter(id=int(validated_data['persona_para_matricular'])).first()
        numero_semestre = usuario.persona.semestre.numero_semestre+1
        if usuario.persona.creditos_aprobados_semestre > usuario.persona.semestre.creditos_permitidos:
            semestre_a_matricular = Semestre.objects.filter(
                numero_semestre=numero_semestre,
                plan_estudio=usuario.persona.semestre.plan_estudio
            ).first()
            if semestre_a_matricular is not None:
                usuario.persona.semestre_a_matricular = semestre_a_matricular
                usuario.persona.creditos_aprobados_semestre = 0
                usuario.save()
                return recibo_por_pagar_nuevo_estudiante(
                    usuario.persona,
                    semestre_a_matricular.id
                )
            else:
                return None
        else:
            return recibo_por_pagar_nuevo_estudiante(
                    usuario.persona,
                    usuario.persona.semestre
                )


class CrearUsuarioEstudianteSerializer(serializers.Serializer):

    codigo = serializers.IntegerField()
    correo_electronico = serializers.EmailField(allow_blank=None)

    def validate_correo_electronico(self, value):
        validador = correo_valido(value)
        if validador[0] or validador[1] is None:
            raise serializers.ValidationError('El correo ya existe registrado o no es válido.')
        else:
            return value

    def validate_codigo(self, value):
        recibo = PagoRecibo.objects.filter(
            codigo=value
        ).first()
        if recibo is not None:
            if recibo.esta_pago == True:
                return value
            else:
                raise serializers.ValidationError('El codigo de recibo no se encuentra pago.')
        else:
            raise serializers.ValidationError('El codigo de recibo no existe.')


    def create(self, validated_data):
        recibo = PagoRecibo.objects.filter(
            codigo=validated_data['codigo']
        ).first()
        
        usuario = crear_usuario(recibo.persona, validated_data['correo_electronico'], 'Estudiante')
        return {
            'usuario': usuario[0].id,
            'password': usuario[1],
        }
    


class SimuladorPagoReciboSerializer(serializers.ModelSerializer):

    codigo_recibo = serializers.IntegerField(max_value=99999999, min_value=10000000)

    class Meta:
        model = TarjetaCredito
        fields = ['codigo_recibo', 'banco', 'numero_tarjeta', 'propietario', 'codigo_seguridad','codigo_recibo']

    def validate_codigo_recibo(self, value):
        if PagoRecibo.objects.filter(codigo=value).exists():
            return value
        else:
            raise serializers.ValidationError('El codigo de recibo no existe.')

    def validate(self, data):
        
        if validar_tarjeta_credito(data['banco'], data['numero_tarjeta'], data['codigo_seguridad'], data['propietario']):
            return data
        else:
            raise serializers.ValidationError('Los datos suministrados para la tarjeta de crédito son incorrectos.')

    def create(self, validated_data):
        tarjeta_credito = TarjetaCredito.objects.filter(
            numero_tarjeta=validated_data['numero_tarjeta'],
            codigo_seguridad=validated_data['codigo_seguridad']
        ).first()
        saldo_total = int(tarjeta_credito.saldo) + int(tarjeta_credito.credito_maximo)
        recibo = PagoRecibo.objects.filter(
            codigo=validated_data['codigo_recibo']
        ).first()
        if saldo_total > recibo.semestre.costo:
            tarjeta_credito.saldo = tarjeta_credito.saldo-recibo.semestre.costo
            tarjeta_credito.save()
            crear_asignaturas_usuario(recibo)
            return recibo
        else:
            raise serializers.ValidationError('La tarjeta no tiene fondos suficientes')
            



class EleccionHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAsignatura
        fields = ['id', 'docente', 'hora_inicio', 'hora_final']
    
    def create(self, validated_data):
        horario = agregar_horario_asignatura(self.context['id_asignatura_usuario'], validated_data['id'])
        return horario.asignatura


class AsignarNotaAsignaturaSerializer(serializers.Serializer):
    CORTES_ASIGNATURA = (
        ('CORTE_1', 'Corte 1'),
        ('CORTE_2', 'Corte 2'),
        ('CORTE_3', 'Corte 3')
    )

    corte_asignatura = serializers.ChoiceField(choices=CORTES_ASIGNATURA)
    nota_corte = serializers.IntegerField(max_value=100)

    def create(self, validated_data):
        return agregar_nota_corte_correspondiente(validated_data['corte_asignatura'], validated_data['nota_corte'])

class EleccionTipoEstudiantePorMatricularSerializer(serializers.Serializer):

    TIPOS_ESTUDIANTE = (
        ('ESTUDIANTE_NUEVO', 'Estudiante nuevo'),
        ('ESTUDIANTE_ANTIGUO', 'Estudiante antiguo')
    )

    tipo_estudiante = serializers.ChoiceField(choices=TIPOS_ESTUDIANTE)

    def validate_tipo_estudiante(self, value):
        if value is not None:
            return value
        else:
            raise serializers.ValidationError('Elije el tipo de estudiante.')

    def create(self, validated_data):
        return validated_data['tipo_estudiante']


class EleccionAsignaturaPorMatricularSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaUsuario
        fields = ['id', 'asignatura', 'usuario']

    def create(self, validated_data):
        asignatura_usuario = AsignaturaUsuario.objects.filter(
            usuario=validated_data['usuario'], 
            asignatura=validated_data['asignatura']
        ).values_list('id', flat=True).first()
        return asignatura_usuario

class EleccionProgramaGenerarReciboSerializer(serializers.Serializer):
    programa = serializers.ChoiceField(choices=Programa.objects.all())

    def create(self, validated_data):
        return validated_data['programa']

class EleccionTipoUsuarioSerializer(serializers.Serializer):

    TIPOS_USUARIO = (
        ('DOCENTE', 'Docente'),
        ('ESTUDIANTE', 'Estudiante')
    )

    tipo_usuario = serializers.ChoiceField(choices=TIPOS_USUARIO)

    def validate_tipo_usuario(self, value):
        if value is not None:
            return value
        else:
            raise serializers.ValidationError('Elije el tipo de estudiante.')

    def create(self, validated_data):
        return validated_data['tipo_usuario']

class EleccionAsignaturaAsignarNotaCorteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaUsuario
        fields = ['asignatura', 'usuario', 'activo', 'aprobado']

    def validate(self, data):
        if AsignaturaUsuario.objects.filter(
            asignatura=data['asignatura'],
            usuario=data['usuario'],
            activo=data['activo'],
            aprobado=data['aprobado']
        ).exists():
            return data
        else:
            raise serializers.ValidationError('No existe una asignatura usuario con lo datos suministrados, por favor verificar.')

    def create(self, validated_data):
        return AsignaturaUsuario.objects.get(
            asignatura=validated_data['asignatura'],
            usuario=validated_data['usuario'],
            activo=validated_data['activo'],
            aprobado=validated_data['aprobado']
        )
    









