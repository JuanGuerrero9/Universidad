import re

from apps.usuario.models import * 
from .models import *


def obtencion_asignaturas(usuario):

    ''' 
    Recibe como parametro el usuario y verifica si existen 
    asignaturas asociadas al semestre que registra el usuario.
    '''

    asignaturas_semestre = list(Asignatura.objects.filter(
        semestre=usuario.persona.semestre
    ).values_list('id', flat=True))

    return AsignaturaUsuario.objects.filter(
        usuario=usuario, 
        asignatura__in=asignaturas_semestre, 
        activo=True
    ).exists()

def recibo_nuevo_semestre(usuario):

    # Crea una instancia del modelo PagoRecibo, generando un codigo de recibo a pagar.

    return PagoRecibo.objects.create(
        semestre=usuario.persona.semestre,
        persona=usuario.persona,
        codigo=randint(1000000, 9999999)
    )

def crear_persona(nombres, apellidos, cedula_ciudadano):

    # Crea una instancia del modelo Persona.

    return Persona.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        cedula_ciudadano=cedula_ciudadano
    )

def recibo_por_pagar_nuevo_estudiante(persona, semestre):

    # Recibe como parametros datos del nuevo estudiante, crea una instancia de la persona y le genera un recibo por pagar.

    if Semestre.objects.filter(id=semestre).exists():
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

def crear_asignaturas_usuario(usuario,recibo):

    # Por cada asignatura del semestre perteneciente al recibo pago, se crean asignaturas para el usuario.

    asignaturas = Asignatura.objects.filter(semestre=recibo.semestre.id)
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

    # Devuelve la tarjeta de credito correspondiente con los parámetros otorgados.

    return TarjetaCredito.objects.filter(
        numero_tarjeta=int(numero_tarjeta),
        banco=Bancos.objects.filter(id=banco_id).first(),
        codigo_seguridad=int(codigo_seguridad),
        propietario=propietario
    ).first()
    
def verificacion_aprobacion_asignaturas_antecesoras(
        listado_asignaturas_usuario_antecesoras, 
        listado_asignaturas_usuario, 
        asignaturas_antecesoras,
        usuario
    ):

    ''' 
    Se verifica que la asignatura que antecede a la que se va a matricular esté aprobada, sino la que se va a
    matricular se desactiva y la antecesora si existe se activa para que se pueda aprobar.
    '''

    for asignatura in listado_asignaturas_usuario_antecesoras:
        if asignatura.aprobado == False:
            listado_asignaturas_usuario.get(
                usuario=usuario,
                asignatura__in=asignaturas_antecesoras
            ).update(activo=False)
            asignatura.activo=True
            asignatura.save()

def obtener_asignaturas_activas(usuario):

    # Filtra las asignaturas que están activas y que aún no tengan un horario asignado.

    return AsignaturaUsuario.objects.filter(
        usuario=usuario,
        activo=True,
        horario_asignatura=None
    )

def obtener_asignaturas_matriculables(usuario):

    # Se obtienen únicamente las asignaturas que el usuario puede matricular.

    asignaturas_usuario = AsignaturaUsuario.objects.filter(usuario=usuario)
    asignaturas_antecesoras = Asignatura.objects.filter(antecesora__in=asignaturas_usuario.filter(
            activo=True
        ).values_list('asignatura')
    )
    if asignaturas_antecesoras is not None:
        listado_asignaturas_usuario_antecesoras = asignaturas_usuario.filter(
            usuario=usuario,
            activo=False,
            asignatura__in=asignaturas_antecesoras
        )
        if len(listado_asignaturas_usuario_antecesoras) > 0:
            verificacion_aprobacion_asignaturas_antecesoras(
                listado_asignaturas_usuario_antecesoras, 
                asignaturas_usuario, 
                asignaturas_antecesoras,
                usuario
            )
            return obtener_asignaturas_activas(usuario)
        else:
            return obtener_asignaturas_activas(usuario)
    else:
        return obtener_asignaturas_activas(usuario)

