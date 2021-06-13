from django import forms
from apps.usuario.models import Persona


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