
import re

from rest_framework.authentication import get_authorization_header
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer



from apps.usuario.models import * 
from apps.institucional.models import *

from django.contrib.auth.models import User, AnonymousUser

def recibo_por_pagar_estudiante_antiguo(persona, semestre):

    # Recibe como parametros datos del antiguo estudiante, crea una instancia de la persona y le genera un recibo por pagar.

    if Semestre.objects.filter(id=semestre).exists():
        recibo = PagoRecibo.objects.create(
            codigo=randint(10000000, 99999999),
            semestre=Semestre.objects.filter(id=semestre).first(),
            persona=persona
        )
        lista = {
            'persona': f'{persona.nombres} {persona.apellidos}',
            'codigo': recibo.codigo
        }

        

def crear_persona(nombres, apellidos, cedula_ciudadano):

    # Crea una instancia del modelo Persona.

    return Persona.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        cedula_ciudadano=cedula_ciudadano
    )

def recibo_por_pagar_nuevo_estudiante(persona, semestre):

    # Recibe como parametros datos del nuevo estudiante, crea una instancia de la persona y le genera un recibo por pagar.

    return PagoRecibo.objects.create(
        codigo=randint(10000000, 99999999),
        semestre=Semestre.objects.filter(id=semestre).first(),
        persona=persona
    )

def correo_valido(correo):

    # Verifica en primera instancia si el correo está asociado a un usuario y segundo si el correo es válido.

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return Usuario.objects.filter(email=correo).exists(), re.search(regex, correo)

def asignar_rol_usuario(usuario, nombre_rol):

    # Recibe el rol que desea crearsele al usuario y se lo enlaza, dandole los permisos y el grupo que los contiene.
    
    if Usuario.objects.filter(id=usuario).exists():
        if Rol.objects.filter(nombre__iexact=nombre_rol).exists():
            Usuario.objects.filter(
                id=usuario
            ).update(
                rol=Rol.objects.filter(nombre__iexact=nombre_rol
            ).first())
        else:
            Usuario.objects.filter(id=usuario).update(
                rol=Rol.objects.create(nombre=nombre_rol)
            )

def crear_usuario(persona, correo, rol):

    # Crea un usuario nuevo y le asigna las materias correspondientes al recibo que se paga.

    password = str(randint(1000000, 9999999))
    nuevo_usuario= Usuario.objects.create(
        username=f'{persona.nombres.replace(" ", "")}_{randint(1000,9999)}',
        password=password,
        email=correo,
        persona=persona
    )
    nuevo_usuario.set_password(password)
    nuevo_usuario.save()
    asignar_rol_usuario(nuevo_usuario.id, rol)
    return nuevo_usuario, password

def validar_tarjeta_credito(banco_id,numero_tarjeta,codigo_seguridad,propietario):

    # Devuelve un booleano que valida la existencia y posibilidad de pagar el recibo

    return TarjetaCredito.objects.filter(
        numero_tarjeta=int(numero_tarjeta),
        banco=Bancos.objects.filter(id=banco_id.id).first(),
        codigo_seguridad=int(codigo_seguridad),
        propietario=propietario
    ).exists()

def obtener_asignaturas_activas(usuario):

    # Filtra las asignaturas que están activas y que aún no tengan un horario asignado.

    return AsignaturaUsuario.objects.filter(
        usuario=usuario,
        activo=True,
        horario_asignatura=None
    )

def obtener_asignaturas_matriculables(usuario):

    # Se obtienen únicamente las asignaturas que el usuario puede matricular.
    
    asignaturas_usuario = AsignaturaUsuario.objects.filter(
        usuario=usuario.id,
        activo=True
    )
    asignaturas_sin_antecesoras, asignaturas_con_antecesoras = [], []
    for asignatura in asignaturas_usuario:
        if asignatura.asignatura.antecesora == None:
            asignaturas_sin_antecesoras.append(asignatura.asignatura.antecesora)
        else:
            asignaturas_con_antecesoras.append(asignatura.asignatura.antecesora)
    if len(asignaturas_con_antecesoras) > 0:
        listado_asignaturas_usuario_antecesoras = asignaturas_usuario.filter(
            usuario=usuario,
            activo=False,
            asignatura__in=asignaturas_con_antecesoras
        )
        if len(listado_asignaturas_usuario_antecesoras) > 0:
            verificacion_aprobacion_asignaturas_antecesoras(
                listado_asignaturas_usuario_antecesoras, 
                asignaturas_usuario, 
                asignaturas_con_antecesoras,
                usuario
            )
            return obtener_asignaturas_activas(usuario)
        else:
            return obtener_asignaturas_activas(usuario)
    else:
        return obtener_asignaturas_activas(usuario)

def obtener_horario_asignatura(asignatura):

    return HorarioAsignatura.objects.filter(
        asignatura=AsignaturaUsuario.objects.get(
            id=asignatura
        ).asignatura
    )

def agregar_horario_asignatura(id_asignatura, id_horario):

    # Obtiene la instancia de Asignatura usuario que le actualiza el horario

    return AsignaturaUsuario.objects.filter(
        id=id_asignatura
    ).first().update(
            horario=HorarioAsignatura.objects.filter(
                id=id_horario
            ).first()
        )


def crear_asignaturas_usuario(recibo):

    # Por cada asignatura del semestre perteneciente al recibo pago, se crean asignaturas para el usuario.

    usuario = Usuario.objects.filter(persona=recibo.persona).first()
    asignaturas = Asignatura.objects.filter(semestre=recibo.semestre.id)
    recibo.esta_pago = True
    recibo.save()
    usuario.persona.semestre = recibo.semestre
    usuario.persona.save()
    asignaturas_usuario = []
    for asignatura in asignaturas:
        asignaturas_usuario.append(AsignaturaUsuario(
            usuario=usuario,
            asignatura=asignatura,
            activo=True
            )
        )
    AsignaturaUsuario.objects.bulk_create(asignaturas_usuario)

def agregar_nota_corte_correspondiente(corte, nota_corte):
    if corte[6] == '1':
        return AsignaturaUsuario.objects.get(
                id=self.context['id_asignatura_usuario']
            ).update(nota_corte1=nota_corte, nota1_agregada=True)
    elif corte[6] == '2':
        return AsignaturaUsuario.objects.get(id=self.context['id_asignatura_usuario']).update(
                nota_corte2=nota_corte,
                nota2_agregada=True
            )
    elif corte[6] == '3':
        return AsignaturaUsuario.objects.get(id=self.context['id_asignatura_usuario']).update(
                nota_corte3=validated_data['nota_corte'],
                nota3_agregada=True
            )

