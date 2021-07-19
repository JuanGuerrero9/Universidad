from django import forms

from apps.usuario.models import Persona
from apps.institucional.models import Programa, Semestre, TarjetaCredito, Cortes


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
                attrs= {
                    'class': 'form-control'
                }
            ),
            'apellidos': forms.TextInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'cedula_ciudadano': forms.NumberInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'imagen': forms.FileInput(
                attrs= {
                    'class': 'form-control'
                }
            )
        }


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

class ProgramaForm(forms.ModelForm):
    programas = forms.ChoiceField(choices=[(doc.id_programa, doc.nombre) for doc in Programa.objects.all()])
    class Meta:
        model = Programa
        fields = ('programas',)
        labels = {
            'programas': 'Elegir un programa'
        }
        widgets = {
            'programas': forms.Select(attrs={'class': 'select'})
        }

class SemestreForm(forms.ModelForm):
    semestre = forms.ChoiceField(choices=[(doc.id_semestre, doc.nombre) for doc in Semestre.objects.all()])
    class Meta:
        model = Semestre
        fields = ('semestre',)
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
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'XXXX-XXXX-XXXX-XXXX'
                }
            ),
            'codigo_seguridad': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese el codigo en la parte trasera de su tarjeta'
                }
            ),
            'programas': forms.Select(attrs={'class': 'select'})
        }


class ActualizarUsuarioForm(forms.ModelForm):

    class Meta:

        model = Cortes
        fields = ['nota_corte1','nota_corte2','nota_corte3']
        labels = {
            'nota_corte1': 'Nota del corte 1',
            'nota_corte2': 'Nota del corte 2',
            'nota_corte3': 'Nota del corte 3'
        }
        widgets = {
            'nota_corte1': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 1'
                }
            ),
            'nota_corte2': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 2'
                }
            ),
            'nota_corte3': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese nota corte 3'
                }
            )
        }