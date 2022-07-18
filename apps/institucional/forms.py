from django import forms

from apps.usuario.models import Persona, Usuario
from apps.institucional.models import *


class PersonaForm(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano', 'imagen']
        labels = {
            'nombres': 'Nombres del usuario',
            'apellidos': 'Apellidos del usuario',
            'cedula_ciudadano': 'Cedula de Ciudadania del Estudiante',
            'imagen': 'Seleccione una imagen nueva para el usuario'
        }
        
        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'cedula_ciudadano': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class NuevoUsuarioDocenteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano']
        labels = {
            'nombres': 'Nombres del usuario',
            'apellidos': 'Apellidos del usuario',
            'cedula_ciudadano': 'Cedula de Ciudadania del Estudiante'
        }
        widgets = {
            'nombres': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres completos'
                }
            ),
            'apellidos': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos completos'
                }
            ),
            'cedula_ciudadano': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Digite su cedula de ciudadania'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super(NuevoUsuarioDocenteForm, self).__init__(*args, **kwargs)
        self.fields['correo_electronico'] = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder': 'example@hotmail.com'}))

class NuevoUsuarioEstudianteForm(forms.ModelForm):
    class Meta:
        model = PagoRecibo
        fields = ('codigo',)
        labels = {
            'codigo': 'Digite el codigo de recibo'
        }
        widgets = {
            'codigo': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '# de Codigo'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(NuevoUsuarioEstudianteForm, self).__init__(*args, **kwargs)
        self.fields['correo_electronico'] = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder': 'example@hotmail.com'}))

class NuevoEstudianteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'cedula_ciudadano']
        labels = {
            'nombres': 'Nombres del usuario',
            'apellidos': 'Apellidos del usuario',
            'cedula_ciudadano': 'Cedula de Ciudadania del Estudiante'
        }
        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres completos'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos completos'
                }
            ),
            'cedula_ciudadano': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite su cedula de ciudadania'
                }
            )
        }
    
    def __init__(self, programa, *args, **kwargs):
        super(NuevoEstudianteForm, self).__init__(*args, **kwargs)
        programa_obt = Programa.objects.filter(id=programa).first()
        plan_estudio_obt = PlanEstudio.objects.filter(programa=programa_obt).first()
        semestres = Semestre.objects.filter(plan_estudio=plan_estudio_obt)
        semestres_validos = [(i.id, i.nombre) for i in semestres]
        self.fields['semestre'] = forms.ChoiceField(choices=semestres_validos,widget=forms.Select(attrs={'class':'form-control'}))

     


class ProgramaForm(forms.ModelForm):
    programas = forms.ChoiceField(choices=[(doc.id, doc.nombre) for doc in Programa.objects.all()])
    class Meta:
        model = Programa
        fields = ('nombre',)
        labels = {
            'programas': 'Elegir un programa'
        }
        widgets = {
            'programas': forms.Select(attrs={'class': 'select'})
        }

class SemestreForm(forms.ModelForm):
    semestre = forms.ChoiceField(choices=[(doc.id, doc.nombre) for doc in Semestre.objects.all()])
    class Meta:
        model = Semestre
        fields = ('nombre',)
        labels = {
            'semestre': 'Elegir un semestre'
        }
        widgets = {
            'semestre': forms.Select(attrs={'class': 'form-select'})
        }


class TarjetaCreditoForm(forms.ModelForm):
    class Meta:
        model = TarjetaCredito
        fields = ['numero_tarjeta','codigo_seguridad','banco']
        labels = {
            'numero_tarjeta': 'Numero de la tarjeta de Credito',
            'codigo_seguridad': 'CVC CODIGO',
            'banco': 'Banco al que pertenece la tarjeta de credito'
        }
        widgets = {
            'numero_tarjeta': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'XXXX-XXXX-XXXX-XXXX'
                }
            ),
            'codigo_seguridad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el codigo en la parte trasera de su tarjeta'
                }
            ),
            'programas': forms.Select(attrs={'class': 'select'})
        }


class ActualizarNotasForm(forms.ModelForm):

    class Meta:

        model = AsignaturaUsuario
        fields = ['nota_corte1','nota_corte2','nota_corte3']
        labels = {
            'nota_corte1': 'Nota del corte 1',
            'nota_corte2': 'Nota del corte 2',
            'nota_corte3': 'Nota del corte 3'
        }
        widgets = {
            'nota_corte1': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 1'
                }
            ),
            'nota_corte2': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 2'
                }
            ),
            'nota_corte3': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 3'
                }
            )
        }


class HorarioEstudianteForm(forms.ModelForm):
    class Meta:
        model = HorarioAsignatura
        fields = ('hora_inicio',)

    def __init__(self, asignatura_id,usuario,*args, **kwargs):
        super(HorarioEstudianteForm, self).__init__(*args, **kwargs)
        asignatura = AsignaturaUsuario.objects.filter(id=asignatura_id, usuario=usuario).first()
        if HorarioAsignatura.objects.filter(asignatura=asignatura.asignatura).exists():
            horarios = HorarioAsignatura.objects.filter(asignatura=asignatura.asignatura)
            horarios_validos = [(i.id, f'{i.hora_inicio} {i.hora_final} {i.asignatura}') for i in horarios]
            self.fields['horarios'] = forms.ChoiceField(choices=horarios_validos,widget=forms.Select(attrs={'class':'form-control'}))