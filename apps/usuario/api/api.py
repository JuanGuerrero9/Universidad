from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework import permissions
from apps.usuario.models import Usuario
from .serializers import UsuarioSerializer, UsuarioLoginSerializer


class UsuarioViewSet(viewsets.GenericViewSet):

    queryset = Usuario.objects.filter(is_active=True)
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario, token = serializer.save()
        data = {
            'usuario': UserModelSerializer(usuario).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

