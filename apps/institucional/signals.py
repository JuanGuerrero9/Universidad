from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .functions import *
from .models import *


@receiver(post_save, sender=AsignaturaUsuario)
def validador_aprobacion_materia(sender, instance, **kwargs):
    if instance.nota1_agregada and instance.nota2_agregada and instance.nota3_agregada:
        nota1_porcentuada = (instance.nota_corte1*instance.porcentaje_corte1_y_2)/100
        nota2_porcentuada = (instance.nota_corte2*instance.porcentaje_corte1_y_2)/100
        nota3_porcentuada = (instance.nota_corte3*instance.porcentaje_corte3)/100
        nota_final = nota1_porcentuada+nota2_porcentuada+nota3_porcentuada
        if nota_final >= 60:
            AsignaturaUsuario.objects.filter(id=instance.id).update(aprobado=True, activo=False, nota_final=nota_final)
        else:
            AsignaturaUsuario.objects.filter(id=instance.id).update(activo=False, nota_final=nota_final)

            
@receiver(post_save, sender=AsignaturaUsuario)
def validador_aprobacion_semestre(sender, instance, **kwargs):
    if instance.aprobado:
        AsignaturaUsuario.objects.get(id=instance.id).update(activo=False)
        Persona.objects.filter(id=instance.usuario.persona.id).first().update(
            creditos_aprobados_semestre=instance.asignatura.creditos+instance.usuario.persona.creditos_aprobados_semestre,
        )
        if not obtencion_asignaturas(instance.usuario):
            if instance.usuario.persona.creditos_aprobados_semestre > (instance.usuario.persona.semestre.creditos_permitidos/2):
                nro_semestre_actual = instance.usuario.persona.semestre.numero_semestre
                nro_semestre_actual += 1
                semestre_aprobado = Semestre.objects.filter(
                    numero_semestre=nro_semestre_actual, 
                    plan_estudio=instance.usuario.persona.semestre.plan_estudio
                ).first()
                if semestre_aprobado:
                    Persona.objects.filter(id=instance.usuario.persona.id).first().update(semestre=semestre_aprobado, creditos_aprobados_semestre=0)


@receiver(post_save, sender=PagoRecibo)
def validador_aprobacion_semestre(sender, instance, **kwargs):
    if instance.esta_pago:
        usuario = Usuario.objects.filter(persona=instance.persona).first()
        if usuario:
            asignaturas_semestre_nuevo = Asignatura.objects.filter(semestre=instance.semestre)
            for asignatura in asignaturas_semestre_nuevo:
                AsignaturaUsuario.objects.create(
                    asignatura=asignatura,
                    usuario=usuario,
                    activo=True
                )
            if usuario.persona.creditos_aprobados_semestre != 0:
                Persona.objects.filter(id=usuario.persona.id).first().update(creditos_aprobados_semestre=0)


    
        





