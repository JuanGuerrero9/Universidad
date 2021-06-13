from rest_framework import serializers
from django.contrib.auth import password_validation, authenticate
from apps.usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'email', 'codigo_universitario']




class UsuarioLoginSerializer(serializers.ModelSerializer):

    def validacion(self, data):

        usuario = authenticate(nombre_usuario= data['nombre_usuario'], password= data['password'])
        if not usuario:
            raise serializers.ValidationError('El usuario o la contraseña se encuentran de manera incorrecta')

        self.context['usuario'] = usuario
        return data


    def crear(self, data):
        token, created= Token.objects.get_or_create(user= self.context['usuario'])
        return self.context['usuario'], token.key




























'''






class CrearUsuarioSerializer(serializers.ModelSerializer):

    password2= serializers.CharField(style={'input-type': 'password'}, write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'nombres', 'apellidos', 'email', 'imagen','password','password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        cuenta= Usuario (
            username=self.validated_data['username'],
            nombres=self.validated_data['nombres'],
            apellidos=self.validated_data['apellidos'],
            email=self.validated_data['email'],
            imagen=self.validated_data['imagen'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Contrasenias no coinciden'})
        cuenta.set_password(password)
        cuenta.save()
        return cuenta





'''

