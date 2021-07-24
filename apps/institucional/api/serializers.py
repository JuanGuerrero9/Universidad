from random import randint

from rest_framework import serializers

from apps.institucional.models import *
from apps.usuario.models import *

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


class CrearUsuarioSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length= None, allow_blank= None)

    class Meta:
        model = PagoRecibo
        fields = ['email', 'codigo']

    def create(self, validated_data):
        try:
            rol = Rol.objects.filter(nombre__iexact = 'Estudiante').first()
        except:
            permisos_defecto = ['add', 'change', 'delete', 'view']
            nuevo_grupo, creado= Group.objects.get_or_create(
                name = 'Estudiante'
                )
            permiso_nuevo = []
            for permiso in permisos_defecto:
                permiso_nuevo.append(Permission.objects.get_or_create(
                    name= f'Can {permiso} estudiante',
                    content_type= ContentType.objects.get_for_model(Rol),
                    codename= f'{permiso}_estudiante'
                ))
            if creado:
                for permisos in permiso_nuevo:
                    nuevo_grupo.permissions.add(permisos[0].id)
                    nuevo_grupo.save()
            rol = Rol.objects.filter(nombre__iexact = 'Estudiante').first()
        recibo = PagoRecibo.ojects.filter(codigo= validated_data['codigo']).first()
        persona = Persona.objects.filter(id_persona = recibo.persona.id_persona).first()
        password = str(randint(100000, 9999999))
        pass_guardada = password
        nuevo_usuario, created = Usuario.objects.get_or_create(
            username             = f'{persona.nombres.replace(" ", "")}_{randint(1000,9999)}',
            password             = password,
            codigo_universitario = randint(1000000, 9999999),
            email                = validated_data['email'],
            persona              = persona,
            rol                  = rol

        )
        if created:
            nuevo_usuario.set_password(password)
            nuevo_usuario.save()
        usuario = nuevo_usuario.id
        asignaturas = Asignatura.objects.filter(semestre= recibo.semestre.id_semestre)
        for asignatura in asignaturas:
            UserAsignatura, _ = AsignaturaUsuario.objects.get_or_create(
                usuario     = nuevo_usuario,
                asignatura  = asignatura,
                activo      = True
            )
            cortes, _ = Cortes.objects.get_or_create(
                asignatura_usuario = UserAsignatura
            )
            notafinal, _ = NotaFinal.objects.get_or_create(
                cortes     = cortes,
                asignatura = UserAsignatura
            )
        context = {
            'usuario': nuevo_usuario,
            'password': pass_guardada
        }
        return context


class SimuladorPagoReciboSerializer(serializers.ModelSerializer):

    codigo_recibo = serializers.IntegerField(max_value= 99999999, min_value= 10000000)

    class Meta:
        model = TarjetaCredito
        fields = ['codigo_recibo', 'banco', 'numero_tarjeta', 'propietario', 'codigo_seguridad']

    def validate_codigo_recibo(self, value):
        try:
            recibo = PagoRecibo.objects.filter(
                codigo= value
            ).first()
        except:
            recibo = None
        if recibo is None or recibo.esta_pago == True:
            raise serializers.ValidationError('El codigo de recibo no es correcto o se encuentra pago')
        return value

    def validate(self, data):
        banco = Bancos.objects.filter(id_banco = data['banco']).first()
        try:
            tarjeta_credito = TarjetaCredito.objects.filter(
                numero_tarjeta= int(data['numero_tarjeta']),
                banco= banco,
                codigo_seguridad= int(data['codigo_seguridad']),
                propietario= data['propietario']
            ).first()
        except:
            tarjeta_credito = None
        if tarjeta_credito is None:
            raise serializers.ValidationError('Verifique los datos suministrados de la tarjeta, alguno es incorrecto')
        return data

    def create(self, validated_data):
        banco = Bancos.objects.filter(id_banco = validated_data['banco']).first()
        try:
            tarjeta_credito = TarjetaCredito.objects.filter(
                numero_tarjeta= int(validated_data['numero_tarjeta']),
                banco= banco,
                codigo_seguridad= int(validated_data['codigo_seguridad']),
                propietario= validated_data['propietario']
            ).first()
        except:
            tarjeta_credito = None
        if tarjeta_credito is not None:
            semestre = Semestre.objects.filter(id_semestre= recibo.semestre.id_semestre).first()
            saldo_total = int(tarjeta_credito.saldo) + int(tarjeta_credito.credito_maximo)
            if saldo_total > int(semestre.costo):
                tarjeta_credito.saldo = tarjeta_credito.saldo - semestre.costo
                recibo = PagoRecibo.objects.filter(
                    codigo= validated_data['codigo_recibo']
                ).first()
                recibo.esta_pago = True
                context = {
                    'tarjeta_credito': tarjeta_credito,
                    'recibo': recibo
                }
                return context