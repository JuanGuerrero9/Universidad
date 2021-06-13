import random
from random import randint

from django.urls import reverse
from django.template import Context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, UpdateView
from django.views.decorators.http import require_http_methods

from apps.institucional.models import *
from apps.usuario.models import Persona, Usuario
from apps.institucional.forms import PersonaForm


class UsuarioNuevo(TemplateView):
    model = Usuario
    template_name = 'Usuario/usuario_creado.html'

    def get_queryset(self, usuario):
        queryset = self.model.objects.filter(id = usuario).first()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['usuario'] = self.get_queryset(self.kwargs['usuario'])
        context['password'] = self.kwargs['password']
        return context  

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class Recibo(TemplateView):

    template_name = 'Institucional/recibo.html'

    def get(self, request, *args, **kwargs):
        print(self.kwargs['recibo'])
        variables = self.kwargs['recibo']
        datos = PagoRecibo.objects.get(id_pago_recibo= variables)
        context= {
            'recibo':datos
        }
        return render(request, self.template_name, context)


class RevisarNotas(TemplateView):

    template_name = 'Institucional/revisar_notas.html'

    def get(self, request, *args, **kwargs):
        usuarios = AsignaturaUsuario.objects.filter(usuario= request.user)
        notas = []
        for usuario in usuarios:
            notas.append(NotaFinal.objects.filter(asignatura= usuario))
            #notas += NotaFinal.objects.filter(asignatura= i)
        context = {
            'notas': notas
        }
        return render(request, self.template_name, context)




class DatosCrearUsuario(TemplateView):

    template_name = 'Usuario/datos_crear_usuario.html'

    def post(self, request, *args, **kwargs):
        recibo = PagoRecibo.objects.filter(codigo = request.POST['recibo_codigo']).first()
        if recibo:
            persona = Persona.objects.filter(id_persona= recibo.persona.id_persona).first()

            if recibo.esta_pago:
                password = str(randint(1000000, 9999999))
                nuevo_usuario, created = Usuario.objects.get_or_create(
                    username             = f'{persona.nombres.replace(" ", "")}_{randint(1000,9999)}',
                    password             = password,
                    codigo_universitario = randint(1000000, 9999999),
                    email                = request.POST['persona_correo_electronico'],
                    persona              = persona

                )
                
                if created:
                    nuevo_usuario.set_password(password)
                    nuevo_usuario.save()
                
                usuario = nuevo_usuario.id
                asignaturas = Asignatura.objects.filter(semestre= recibo.semestre.id_semestre)
                
                for i in asignaturas:
                    UserAsignatura, created = AsignaturaUsuario.objects.get_or_create(
                        usuario     = request.user,
                        asignatura  = i
                    )
                    cortes, _ = Cortes.objects.get_or_create(
                        asignatura_usuario = UserAsignatura
                    )
                    notafinal, created3 = NotaFinal.objects.get_or_create(
                        cortes     = cortes,
                        asignatura = UserAsignatura
                    )

                return redirect(reverse('institucional:usuario_creado', kwargs={'usuario':usuario, 'password':password}))
        else:
            return HttpResponse("El codigo de recibo de pago aun no esta cancelado")
        return redirect(reverse('institucional:datos_crear_usuario'))
   

class EstudiantesMatriculados(TemplateView):

    template_name = 'Institucional/estudiantes_matriculados.html'

    def get(self, request, *args, **kwargs):
        usuario = AsignaturaUsuario.objects.filter(horario_asignatura= self.kwargs['horario_estudiantes'])
        context = {
            'usuario': usuario
        }
        return render(request, self.template_name, context)



class HorarioAsignaturas(TemplateView):

    template_name = 'Institucional/horario_asignaturas.html'

    def get(self, request, *args, **kwargs):
        asignaturas = AsignaturaUsuario.objects.filter(usuario= request.user.id)
        context = {}
        
        dias_semana = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
        for asignatura in asignaturas:
            print(asignatura)
            
            dia_numerico = dias_semana.index(f'{asignatura.horario_asignatura.dia_semana.nombre_dia}')
            context += {
                [format(dia_numerico)]: asignatura,
            }
        print(context)
        return render(request, self.template_name, context)



class EditarUsuario(UpdateView):

    model = Persona
    form_class = PersonaForm
    template_name = 'Institucional/editar_usuario.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(id = request.user.id).update(
            username             = request.POST['usuario_username'],
            email                = request.POST['usuario_email'],
            codigo_universitario = request.POST['usuario_codigo']
        )
        formulario = self.get_form(self.form_class)
        if formulario.is_valid():
            formulario.save()
            return HttpResponse('El formulario se ha Actualizado Satisfactoriamente!')
        return redirect(reverse('index'))




class GenerarRecibo(View):

    template_name  = 'Institucional/generar_recibo.html'

    def get(self, request, *args, **kwargs):
        programa = Programa.objects.all()
        semestre = Semestre.objects.all()
        return render(request, self.template_name, {'programa': programa, 'semestre': semestre})

    def post(self, request, *args, **kwargs):

        programa = Programa.objects.all()
        semestre = Semestre.objects.all()

        cedula = request.POST['persona_documento']
        persona, created = Persona.objects.get_or_create(
            nombres          = request.POST['persona_nombre'],
            apellidos        = request.POST['persona_apellido'],
            cedula_ciudadano = int(request.POST['persona_documento'])

        )
        try:
            carrera_persona = int(request.POST['persona_carrera'])
        except:
            carrera_persona = 0
        
        if carrera_persona > 0:
            plan_estudio = PlanEstudio.objects.filter(programa= int(request.POST['persona_carrera'])).first()
            semestre = Semestre.objects.filter(id_semestre = request.POST['persona_semestre']).first()
            recibo_estudiante, creado = PagoRecibo.objects.get_or_create(
                codigo      = randint(10000000, 99999999),
                semestre    = semestre,
                persona     = persona
            )
            recibo= recibo_estudiante.id_pago_recibo
            return redirect(reverse('institucional:recibo', kwargs={'recibo': recibo}))
        else:
            errores = {
                'persona_carrera': 'Debe seleccionar una carrera'
            }
        return render(request, self.template_name, {'programa': programa, 'semestre': semestre})


         

class ElegirHorario(View):

    template_name = 'Institucional/elegir_horario.html'

    def get(self, request, *args, **kwargs):
        asignatura = self.kwargs['asignatura']
        horarios_disponibles = HorarioAsignatura.objects.filter(Asignatura= asignatura)
        context = {
            'horarios': horarios_disponibles
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        asignatura = HorarioAsignatura.objects.get(id_horario=request.POST['asignatura_horario'])
        usuario = AsignaturaUsuario.objects.get(usuario= request.user, asignatura= asignatura.Asignatura)
        usuario.horario_asignatura = asignatura
        usuario.save()
        return redirect(reverse('institucional:matricular_asignaturas'))




class MatricularAsignatura(View):

    template_name = 'Institucional/matricular_asignaturas.html'

    def get(self, request, *args, **kwargs):
        asignaturas_usuario = AsignaturaUsuario.objects.filter(usuario = request.user)
        asignaturas_con_antecesoras = None
        asignaturas_sin_antecesoras = None
        asignaturas_para_matricular = []
        for i in asignaturas_usuario:
            asignaturas_con_antecesoras = AsignaturaAntecesora.objects.filter(antecesora = i.asignatura.id_asignatura)
            asignaturas_sin_antecesoras = asignaturas_con_antecesoras.filter(antecesora = None)#AsignaturaAntecesora.objects.filter(asignatura = i.asignatura.id_asignatura, antecesora = None)
            if asignaturas_sin_antecesoras is not None:
                for f in asignaturas_sin_antecesoras:
                    asignaturas_para_matricular += AsignaturaUsuario.objects.filter(
                        usuario    = request.user,
                        asignatura = f.asignatura,
                        )
            if asignaturas_con_antecesoras is not None:
                for f in asignaturas_con_antecesoras:
                    asignaturas = AsignaturaUsuario.objects.filter(asignatura = f.asignatura.id_asignatura)
                    for m in asignaturas:
                        if asignatura[m].aprobado:
                            asignaturas_para_matricular += AsignaturaUsuario.objects.filter(
                                usuario    = request.user,
                                asignatura = asignatura
                            )
        horarios = AsignaturaUsuario.objects.filter(horario_asignatura= not None)
        context = {
            'asignaturas' : asignaturas_para_matricular,
            'horarios': horarios
        }
        return render(request, self.template_name, context)

    
    def post(self, request, *args, **kwargs):
        asignatura_usuario = AsignaturaUsuario.objects.get(id_asignatura_usuario = request.POST['asignatura_semestre'])
        return redirect(reverse('institucional:elegir_horario', kwargs= {'asignatura': asignatura_usuario.asignatura.id_asignatura}))
                


class EditarNotas(View):

    template_name = 'Institucional/editar_notas.html'

    def get(self, request, *args, **kwargs):
        horario = HorarioAsignatura.objects.get(id_horario= self.kwargs['horario'])
        estudiantes_activos = AsignaturaUsuario.objects.filter(horario_asignatura= horario, activo= True)
        notas = []
        print(estudiantes_activos)
        for i in estudiantes_activos:
            notas = NotaFinal.objects.filter(asignatura= i)
        context = {
            'estudiantes': estudiantes_activos,
            'notas': notas
        }
        return render(request, self.template_name, context)



class ElegirHorarioDocente(View):

    template_name = 'Institucional/elegir_horario_docente.html'

    def get(self, request, *args, **kwargs):
        horarios = HorarioAsignatura.objects.filter(docente= request.user)
        context = {
            'horarios': horarios
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        horario = request.POST['asignatura_horario_docente']
        return redirect(reverse('institucional:editar_notas', kwargs={'horario': horario}))


class HorarioEstudiantesMatriculados(View):

    template_name = 'Institucional/horario_estudiantes_matriculados.html'

    def get(self, request, *args, **kwargs):
        horarios = HorarioAsignatura.objects.filter(docente= request.user)
        context = {
            'horarios': horarios
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        horario = request.POST['horario_estudiantes_matriculados']
        return redirect(reverse('institucional:estudiantes_matriculados', kwargs= {'horario_estudiantes': horario}))