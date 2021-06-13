from django.contrib import admin
from django.contrib.auth.models import Permission
from apps.usuario.models import Usuario, Persona, Rol

admin.site.register(Usuario)
admin.site.register(Persona)
admin.site.register(Rol)
admin.site.register(Permission)