from django import forms

from apps.usuario.models import Persona
from apps.institucional.models import Programa, Semestre


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