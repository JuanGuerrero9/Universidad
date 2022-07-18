import random
import time
import re
from random import randint

from django.urls import reverse
from django.template import Context
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, UpdateView
from django.views.decorators.http import require_http_methods

from apps.institucional.models import *
from apps.usuario.models import Persona, Usuario, Rol
from apps.institucional.forms import *
from apps.institucional.functions import *




class UsuarioNuevo(TemplateView):

    ###  --- Vista donde se imprime el usuario y la contrasenia del nuevo usuario creado. ---

    model = Usuario
    template_name = 'Institucional/funcionario/usuario_creado.html'


class Recibo(TemplateView):

    ###  --- Vista donde se imprime el recibo luego de poner los datos del estudiante. ---

    model = PagoRecibo
    template_name = 'Institucional/funcionario/recibo.html'


class EditarNotas(TemplateView):

    model = HorarioAsignatura
    template_name = 'Institucional/docente/editar_notas.html'

class ReciboPagado(TemplateView):

    template_name = 'Institucional/funcionario/recibo_pagado.html'


class RevisarNotas(TemplateView):

    ###  --- Vista de la pestaña de ESTUDIANTE para observar las notas de las asignaturas matriculadas. ---

    model = AsignaturaUsuario
    template_name = 'Institucional/estudiante/revisar_notas.html'

    def get_queryset(self, usuario):
        queryset = self.model.objects.filter(
            usuario=usuario, 
            horario_asignatura= not None
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context['asignaturas'] = self.get_queryset(self.request.user)
        return context


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())



class HorarioAsignaturas(TemplateView):

    ###  --- Permite observar desde la pestaña de ESTUDIANTE los horarios que tienen las asignaturas ya matriculadas. ---

    model = AsignaturaUsuario
    template_name = 'Institucional/estudiante/horario_asignaturas.html'



class EstudiantesMatriculados(TemplateView):

    ###  --- Renderiza desde la pestaña de DOCENTE los estudiantes matriculados en una asignatura. ---

    model = AsignaturaUsuario
    template_name = 'Institucional/docente/estudiantes_matriculados.html'

    def get_queryset(self, horario):
        queryset = self.model.objects.filter(horario_asignatura__in=horario)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horarios = HorarioAsignatura.objects.filter(docente=self.request.user).values_list('id', flat=True)
        if len(horarios) != 0:
            context['estudiantes'] = []
            context['estudiantes'].append(self.get_queryset(horarios))
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class HorarioDocenteAsignaturas(TemplateView):

    ###  --- Muestra el horario para dictar clases del DOCENTE. ---

    model = HorarioAsignatura
    template_name = 'Institucional/docente/horario_docente_asignaturas.html'

    def get_queryset(self, docente):
        queryset = self.model.objects.filter(docente=docente)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horarios = self.get_queryset(self.request.user)
        context['horarios'] = horarios
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class GenerarRecibo(TemplateView):

    ###  --- Vista que desde la pestaña FUNCIONARIO te permite ingresar los datos para generar un recibo de pago. ---

    form_class = NuevoEstudianteForm
    second_form_class = ProgramaForm

    template_name  = 'Institucional/funcionario/generar_recibo.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['programas'] = Programa.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ActualizarNotas(TemplateView):

    template_name = 'Institucional/docente/actualizar_notas.html'


    # def post(self,request,*args,**kwargs):
    #     if request.is_ajax():
    #         form = self.form_class(request.POST, instance=self.get_object())
    #         if form.is_valid():
    #             form.save()
    #             if form.cleaned_data.get('nota_corte1') != 0:
    #                 asignatura = self.get_object()
    #                 asignatura.nota1_agregada = True
    #                 asignatura.save()
    #             if form.cleaned_data.get('nota_corte2') != 0:
    #                 asignatura = self.get_object()
    #                 asignatura.nota2_agregada = True
    #                 asignatura.save()
    #             if form.cleaned_data.get('nota_corte3') != 0:
    #                 asignatura = self.get_object()
    #                 asignatura.nota3_agregada = True
    #                 asignatura.save()
    #             mensaje = 'Las notas se han actualizado correctamente!'
    #             error = 'No hay error!'
    #             response = JsonResponse({'mensaje': mensaje, 'error': error})
    #             response.status_code = 201
    #             return response
    #         else:
    #             mensaje = 'Las notas no se han podido actualizar!'
    #             error = form.errors
    #             response = JsonResponse({'mensaje': mensaje, 'error': error})
    #             response.status_code = 400
    #             return response
    #     else:
    #         return redirect('index')



class EditarUsuario(UpdateView):

    ###  --- Desde CONFIGURACIÓN DE USUARIO te permite editar los datos del Usuario que ha iniciado sesión. ---

    model = Persona
    form_class = PersonaForm
    template_name = 'Usuario/editar_usuario.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            Usuario.objects.filter(id=request.user.id).update(
            username=request.POST['usuario_username'],
            email=request.POST['usuario_email'],
            )
            formulario = self.form_class(request.POST, instance=self.get_object())
            if formulario.is_valid():
                formulario.save()
                mensaje = 'Se ha actualizado el usuario Correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido actualizar el usuario!'
                error = formulario.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('index')


class CrearUsuarioEstudianteView(View):

    ###  --- Vista que permite validar si esta pago el recibo y posteriormente crear un usuario. ---

    template_name = 'Institucional/funcionario/crear_usuario_estudiante.html'
    form_class = NuevoUsuarioEstudianteForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            correo = correo_valido(request.POST['correo_electronico'])
            if correo[0] == False and correo[1] is not None:
                recibo = PagoRecibo.objects.filter(codigo=request.POST['codigo']).first()
                if recibo:
                    if recibo.esta_pago:
                        usuario_nuevo = crear_usuario(
                            recibo.persona, 
                            request.POST['correo_electronico'],
                            'Estudiante'
                            )
                        crear_asignaturas_usuario(usuario_nuevo[0],recibo)
                        mensaje = 'Usuario creado correctamente!'
                        error = 'No hay errores'
                        response = JsonResponse({'mensaje':mensaje,'error':error, 'url':  f'/institucional/usuario_creado/{usuario_nuevo[0].id}/{usuario_nuevo[1]}/'})
                        return response
                    else:
                        mensaje = 'No se ha podido generar el recibo!'
                        error = 'El recibo no se encuentra pago!'
                        response = JsonResponse({'mensaje':mensaje,'error':error})
                        response.status_code = 400
                        return response
                else:
                    mensaje = 'No se ha podido generar el recibo!'
                    error = 'No existe un recibo con este codigo!'
                    response = JsonResponse({'mensaje':mensaje,'error':error})
                    response.status_code = 400
                    return response
            else:
                mensaje = 'No se ha podido generar el recibo!'
                error = 'El correo ya existe o no es un correo valido!'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('index')


class MatricularEstudianteNuevoView(View):

    # --- Vista que registra a estudiantes nuevos en el sistema. ---

    template_name = 'Institucional/funcionario/matricula_estudiante_nuevo.html'
    form_class = NuevoEstudianteForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class(self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(self.kwargs['pk'], request.POST)
            if form.is_valid():
                persona = crear_persona(
                    form.cleaned_data.get('nombres'),
                    form.cleaned_data.get('apellidos'),
                    form.cleaned_data.get('cedula_ciudadano')
                )

                recibo_por_pagar = recibo_por_pagar_nuevo_estudiante(
                    persona,
                    form.cleaned_data.get('semestre')
                )
                mensaje = 'Recibo creado correctamente!'
                error = 'No hay errores'
                response = JsonResponse({'mensaje':mensaje,'error':error, 'url':  f'/institucional/recibo/{recibo_por_pagar.id}/'})
                return response
            else:
                mensaje = 'No se ha podido generar el recibo!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('index')

class MatricularEstudianteAntiguoView(TemplateView):

    # --- Vista que permite matricular estudiantes antes registrados en el sistema. ---

    template_name = 'Institucional/funcionario/matricula_estudiante_antiguo.html'



class CrearUsuarioDocenteView(View):

    # --- Crea un Usuario que tiene el rol y los permisos de un Docente. ---

    template_name = 'Institucional/funcionario/crear_usuario_docente.html'
    form_class = NuevoUsuarioDocenteForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class
        return context
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form= self.form_class(request.POST)
            if form.is_valid():
                persona = crear_persona(
                    form.cleaned_data.get('nombres'),
                    form.cleaned_data.get('apellidos'),
                    form.cleaned_data.get('cedula_ciudadano')
                )
                usuario_nuevo = crear_usuario(persona, form.cleaned_data.get('correo_electronico'), 'Docente')
                mensaje = 'Usuario creado correctamente!'
                error = 'No hay errores'
                response = JsonResponse({'mensaje':mensaje,'error':error, 'url':  f'/institucional/usuario_creado/{usuario_nuevo[0]}/{usuario_nuevo[1]}/'})
                return response
            else:
                mensaje = 'No se ha podido crear el usuario!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('index')


class ElegirHorarioEstudiante(TemplateView):

    ###  --- Te permite elegir desde la pestaña ESTUDIANTE el horario que deseas ver en la asignatura a matricular. ---

    model = HorarioAsignatura
    template_name = 'Institucional/estudiante/elegir_horario.html'


class SimuladorPagoRecibo(View):

    ###  --- Realiza la simulacion del pago de recibo validando el codigo y el saldo disponible de la tarjeta de credito. ---

    template_name = 'Institucional/funcionario/simulador_pago_recibo.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['bancos'] = Bancos.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            recibo = PagoRecibo.objects.filter(codigo= request.POST['codigo_de_pago']).first()
            if recibo is not None and recibo.esta_pago != True:
                tarjeta_credito = validar_tarjeta_credito(request.POST['banco_tarjeta'],request.POST['numero_tarjeta_credito'],request.POST['codigo_seguridad_tarjeta'],request.POST['propietario_tarjeta'])
                if tarjeta_credito:
                    semestre = Semestre.objects.filter(id=recibo.semestre.id).first()
                    saldo_total = int(tarjeta_credito.saldo) + int(tarjeta_credito.credito_maximo)
                    if saldo_total > int(semestre.costo):
                        tarjeta_credito.saldo = tarjeta_credito.saldo - semestre.costo
                        recibo.esta_pago = True
                        mensaje = 'Desea pagar el recibo con valor de {}?'.format(semestre.costo)
                        error = 'No hay errores'
                        response = JsonResponse({'mensaje':mensaje,'error':error})
                        response.status_code = 201
                        return response
                    else:
                        mensaje = 'No se ha podido pagar el recibo correctamente!'
                        error = 'El saldo de su tarjeta para pagar el recibo es insuficiente!'
                        response = JsonResponse({'mensaje': mensaje, 'error': error})
                        response.status_code = 400
                        return response
                else:
                    mensaje = 'No se ha podido pagar el recibo correctamente!'
                    error = 'Verifique que los datos de la tarjeta de Credito sean correctos!'
                    response = JsonResponse({'mensaje': mensaje, 'error': error})
                    response.status_code = 400
                    return response
            else:
                mensaje = 'No se ha podido pagar el recibo correctamente!'
                error = 'El codigo de recibo no es correcto o ya se encuentra pago!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect(reverse('index'))



class MatricularAsignatura(TemplateView):
    
    ###  --- Desde la pestaña ESTUDIANTE renderiza las asignaturas disponibles a matricular y hace una lista de las ya matriculadas. ---

    template_name = 'Institucional/estudiante/matricular_asignaturas.html'

    




