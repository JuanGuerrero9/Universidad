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
from apps.institucional.forms import PersonaForm, NuevoEstudianteForm, ProgramaForm, SemestreForm, ActualizarUsuarioForm





class UsuarioNuevo(TemplateView):

    ###  --- Vista donde se imprime el usuario y la contrasenia del nuevo usuario creado ---

    model = Usuario
    template_name = 'Institucional/funcionario/usuario_creado.html'

    def get_queryset(self, usuario):
        queryset = self.model.objects.filter(id = usuario).first()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['usuario'] = self.get_queryset(self.kwargs['usuario'])
        context['password'] = self.kwargs['passusuario']
        return context   

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class Recibo(TemplateView):

    ###  --- Vista donde se imprime el recibo luego de poner los datos del estudiante ---

    model = PagoRecibo
    template_name = 'Institucional/funcionario/recibo.html'

    def get_queryset(self, variables):
        queryset = self.model.objects.filter(id_pago_recibo = variables).first()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context['recibo'] = self.get_queryset(self.kwargs['id'])
        context['dia'] = time.strftime("%d, %B de %Y")
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())






class RevisarNotas(TemplateView):

    ###  --- Vista de la pestaña de ESTUDIANTE para observar las notas de las asignaturas matriculadas ---

    model = AsignaturaUsuario
    template_name = 'Institucional/estudiante/revisar_notas.html'

    def get_queryset(self, usuario):
        queryset = self.model.objects.filter(usuario = usuario, activo= True,horario_asignatura= not None)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        asignaturas = self.get_queryset(self.request.user)
        notas = []
        for asignatura in asignaturas:
            notas.append(NotaFinal.objects.filter(asignatura = asignatura))
        context['notas'] = notas
        return context


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())



class HorarioAsignaturas(TemplateView):

    ###  --- Permite observar desde la pestaña de ESTUDIANTE los horarios que tienen las asignaturas ya matriculadas ---

    model = AsignaturaUsuario
    template_name = 'Institucional/estudiante/horario_asignaturas.html'

    def get_context_data(self, **kwargs):
        context = {}
        asignaturas = AsignaturaUsuario.objects.filter(usuario = self.request.user, activo= True, horario_asignatura= not None)
        for asignatura in asignaturas:
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Lunes':
                context['Lunes'] = asignatura
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Martes':
                context['Martes'] = asignatura
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Miercoles':
                context['Miercoles'] = asignatura
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Jueves':
                context['Jueves'] = asignatura
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Viernes':
                context['Viernes'] = asignatura
            if asignatura.horario_asignatura.dia_semana.nombre_dia == 'Sabado':
                context['Sabado'] = asignatura
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class EstudiantesMatriculados(TemplateView):

    ###  --- Renderiza desde la pestaña de DOCENTE los estudiantes matriculados en una asignatura ---

    model = AsignaturaUsuario
    template_name = 'Institucional/docente/estudiantes_matriculados.html'

    def get_queryset(self, horario):
        queryset = self.model.objects.filter(horario_asignatura= horario)

    def get_context_data(self, **kwargs):
        context = {}
        context['usuario'] = self.get_queryset(self.kwargs['horario_estudiantes'])
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class HorarioDocenteAsignaturas(TemplateView):

    ###  --- Muestra el horario para dictar clases del DOCENTE ---

    model = HorarioAsignatura
    template_name = 'Institucional/docente/horario_docente_asignaturas.html'

    def get_queryset(self, docente):
        queryset = self.model.objects.filter(docente = docente)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horarios = self.get_queryset(self.request.user)
        context['horarios'] = horarios
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ActualizarNotas(UpdateView):

    model = Cortes
    form_class = ActualizarUsuarioForm
    template_name = 'Institucional/docente/actualizar_notas.html'

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = 'Las notas se han actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'Las notas no se han podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('index')



class EditarUsuario(UpdateView):

    ###  --- Desde CONFIGURACIÓN DE USUARIO te permite editar los datos del Usuario que ha iniciado sesión ---

    model = Persona
    form_class = PersonaForm
    template_name = 'Usuario/editar_usuario.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            Usuario.objects.filter(id = request.user.id).update(
            username             = request.POST['usuario_username'],
            email                = request.POST['usuario_email'],
            codigo_universitario = request.POST['usuario_codigo']
            )
            formulario = self.form_class(request.POST, instance= self.get_object())
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




class DatosCrearUsuario(View):

    ###  --- Vista que desde la pestaña de FUNCIONARIO te permite ingresar los datos necesarios para generar un usuario ---

    template_name = 'Institucional/funcionario/datos_crear_usuario.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['programa'] = Programa.objects.all()
        context['semestre'] = Semestre.objects.all()
        context['form'] = self.form_class
        context['form2'] = self.second_form_class
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            try:
                email = Usuario.objects.filter(email= request.POST['persona_correo_electronico']).exists()
            except :
                email = True
            if email == False and re.search(regex, request.POST['persona_correo_electronico']) is not None:
                try:
                    recibo = PagoRecibo.objects.filter(codigo = request.POST['recibo_codigo']).first()
                except:
                    recibo = None
                if recibo is not None and recibo.esta_pago:
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
                    persona = Persona.objects.filter(id_persona= recibo.persona.id_persona).first()
                    password = str(randint(1000000, 9999999))
                    pass_guardada = password
                    nuevo_usuario, created = Usuario.objects.get_or_create(
                        username             = f'{persona.nombres.replace(" ", "")}_{randint(1000,9999)}',
                        password             = password,
                        codigo_universitario = randint(1000000, 9999999),
                        email                = request.POST['persona_correo_electronico'],
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
                    mensaje = 'Recibo creado correctamente!'
                    error = 'No hay errores'
                    context = {
                        'usuario' : usuario,
                        'passusuario': pass_guardada,
                        'status': 201
                    }
                    response = JsonResponse({'mensaje':mensaje,'error':error, 'context': context})
                    return response
                else:
                    mensaje = 'No se ha podido generar el recibo!'
                    error = 'El recibo no se encuentra pago!'
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



class GenerarRecibo(View):

    ###  --- Vista que desde la pestaña FUNCIONARIO te permite ingresar los datos para generar un recibo de pago ---

    form_class = NuevoEstudianteForm
    second_form_class = ProgramaForm

    template_name  = 'Institucional/funcionario/generar_recibo.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['programa'] = Programa.objects.all()
        context['semestre'] = Semestre.objects.all()
        context['form'] = self.form_class
        context['form2'] = self.second_form_class
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            formulario1 = self.form_class(request.POST)
            formulario2 = self.second_form_class(request.POST)
            if formulario1.is_valid() and formulario2.is_valid():
                semestre = Semestre.objects.filter(id_semestre=request.POST['semestre_estudiante']).first()
                persona = Persona.objects.filter( 
                            nombres= formulario1.cleaned_data.get('nombres'),
                            apellidos= formulario1.cleaned_data.get('apellidos'),
                            cedula_ciudadano= formulario1.cleaned_data.get('cedula_ciudadano')).first()
                recibo_estudiante, _= PagoRecibo.objects.get_or_create(
                        codigo      = randint(10000000, 99999999),
                        semestre    = semestre,
                        persona     = persona
                )
                mensaje = 'Recibo creado correctamente!'
                error = 'No hay errores'
                context = {
                    'recibo': recibo_estudiante.id_pago_recibo,
                    'status': 201
                }
                response = JsonResponse({'mensaje':mensaje,'error':error, 'context': context})
                return response
            else:
                mensaje = 'No se ha podido generar el recibo!'
                error = formulario1.errors
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('index')
         

class ElegirHorarioEstudiante(View):

    ###  --- Te permite elegir desde la pestaña ESTUDIANTE el horario que deseas ver en la asignatura a matricular ---

    model = HorarioAsignatura
    template_name = 'Institucional/estudiante/elegir_horario.html'

    def get_queryset(self, asignatura):
        queryset = self.model.objects.filter(Asignatura = asignatura)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        asignatura = self.kwargs['asignatura']
        horarios_disponibles = self.get_queryset(asignatura)
        context['horarios'] = horarios_disponibles
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                asignatura = HorarioAsignatura.objects.filter(id_horario=int(request.POST['asignatura_horario'])).first()
            except:
                asignatura = None
            if asignatura != None:
                usuario = AsignaturaUsuario.objects.filter(usuario= request.user, asignatura= asignatura.Asignatura).first()
                usuario.horario_asignatura = asignatura
                usuario.save()
                mensaje = 'Se ha agregado horario a la asignatura correctamente!'
                error = 'No hay errores'
                context = {
                    'status': 201
                }
                response = JsonResponse({'mensaje':mensaje,'error':error, 'context': context})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido añadir un horario a la asignatura!'
                error = 'Debe elegir un horario para la asignatura'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 400
                return response
        else:
            return redirect(reverse('index'))


class SimuladorPagoRecibo(View):

    ###  --- Realiza la simulacion del pago de recibo validando el codigo y el saldo disponible de la tarjeta de credito ---

    template_name = 'Institucional/funcionario/simulador_pago_recibo.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['bancos'] = Bancos.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                recibo = PagoRecibo.objects.filter(
                    codigo= request.POST['codigo_de_pago']
                ).first()
            except:
                recibo = None
            if recibo is not None and recibo.esta_pago != True:
                banco = Bancos.objects.filter(id_banco = request.POST['banco_tarjeta']).first()
                try:
                    tarjeta_credito = TarjetaCredito.objects.filter(
                        numero_tarjeta= int(request.POST['numero_tarjeta_credito']),
                        banco= banco,
                        codigo_seguridad= int(request.POST['codigo_seguridad_tarjeta']),
                        propietario= request.POST['propietario_tarjeta']
                    ).first()
                except:
                    tarjeta_credito = None

                if tarjeta_credito is not None:
                    semestre = Semestre.objects.filter(id_semestre= recibo.semestre.id_semestre).first()
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



class MatricularAsignatura(View):
    
    ###  --- Desde la pestaña ESTUDIANTE renderiza las asignaturas disponibles a matricular y hace una lista de las ya matriculadas ---

    template_name = 'Institucional/estudiante/matricular_asignaturas.html'

    
    def get_context_data(self, usuario, **kwargs):
        context = {}
        asignaturas_usuario = AsignaturaUsuario.objects.filter(usuario = usuario, activo = True)
        asignaturas_antecesoras = []
        asignaturas_con_antecesoras = []
        asignaturas_sin_antecesoras = []
        asignaturas_para_matricular = []
        asignaturas_listas = []
        for asignaturas in asignaturas_usuario:
            asignaturas_con_antecesoras.append(
                AsignaturaAntecesora.objects.filter(antecesora = asignaturas.asignatura.id_asignatura).first()
            )
            asignaturas_sin_antecesoras.append(
                AsignaturaAntecesora.objects.filter(asignatura = asignaturas.asignatura.id_asignatura, antecesora = None).first()
            )
        if asignaturas_sin_antecesoras is not []:
            for asignaturas_sin in asignaturas_sin_antecesoras:
                asignaturas_para_matricular.append(AsignaturaUsuario.objects.filter(
                    usuario    = usuario,
                    asignatura = asignaturas_sin.asignatura,
                    ).first())
        if asignaturas_con_antecesoras is not []:
            for asignaturas_con in asignaturas_con_antecesoras:
                try:
                    asignaturas_antecesoras.append(
                    AsignaturaUsuario.objects.filter(asignatura = asignaturas_con.antecesora.id_antecesora).first()
                    )
                except:
                    pass
        if asignaturas_antecesoras is not []:
            for asignatura in asignaturas_antecesoras:
                if asignatura.aprobado is True:
                    asignaturas_para_matricular.append(AsignaturaUsuario.objects.filter(
                        usuario    = usuario,
                        asignatura = asignatura
                    ).first())
        horarios = AsignaturaUsuario.objects.filter(horario_asignatura= not None)
        for asignaturas_separadas in asignaturas_para_matricular:
            if asignaturas_separadas.horario_asignatura is None:
                asignaturas_listas.append(asignaturas_separadas)

        context['asignaturas'] = asignaturas_listas
        context['horarios'] = horarios
        return context


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(request.user))

    
    def post(self, request, *args, **kwargs):
        asignatura_usuario = AsignaturaUsuario.objects.get(id_asignatura_usuario = request.POST['asignatura_semestre'])
        return redirect(reverse('institucional:elegir_horario', kwargs= {'asignatura': asignatura_usuario.asignatura.id_asignatura}))
                


class EditarNotas(View):

    model = HorarioAsignatura
    template_name = 'Institucional/docente/editar_notas.html'

    def get_queryset(self, horario):
        queryset = self.model.objects.filter(id_horario = horario).first()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horario = self.get_queryset(self.kwargs['horario'])
        estudiantes_activos = AsignaturaUsuario.objects.filter(horario_asignatura = horario, activo= True)
        notas = []
        for estudiante in estudiantes_activos:
            notas.append(NotaFinal.objects.filter(asignatura= estudiante).first())
        context['estudiantes'] = estudiantes_activos
        context['notas'] = notas
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())



class ElegirHorarioDocente(View):
    
    model = HorarioAsignatura
    template_name = 'Institucional/docente/elegir_horario_docente.html'

    def get_queryset(self, docente):
        queryset = self.model.objects.filter(docente = docente)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horarios = self.get_queryset(self.request.user)
        context['horario'] = horarios
        return context


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        horario = request.POST['asignatura_horario_docente']
        return redirect(reverse('institucional:editar_notas', kwargs={'horario': horario}))


class HorarioEstudiantesMatriculados(View):

    model = HorarioAsignatura
    template_name = 'Institucional/docente/horario_estudiantes_matriculados.html'

    def get_queryset(self, docente):
        queryset = self.model.objects.filter(docente = docente)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        horarios = self.get_queryset(self.request.user)
        context['horarios'] = horarios
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        horario = request.POST['horario_estudiantes_matriculados']
        return redirect(reverse('institucional:estudiantes_matriculados', kwargs= {'horario_estudiantes': horario}))


