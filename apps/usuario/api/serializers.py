from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.usuario.models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username','email')




























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

