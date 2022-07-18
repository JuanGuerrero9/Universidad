from django.db import models
from random import randint
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType


class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, False, False,**extra_fields)
    
    def create_superuser(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, True, True,**extra_fields)



class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)   
    nombre = models.CharField('Nombre de rol', max_length=30, unique=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Rols'

    def __str__(self,):
        return self.nombre


    def save(self, *args, **kwargs):
        permisos_defecto = ['add', 'change', 'delete', 'view']
        if not self.id_rol:

            nuevo_grupo, creado= Group.objects.get_or_create(
                name=f'{self.nombre}'
                )
            permiso_nuevo = []
            for permiso in permisos_defecto:
                permiso_nuevo.append(Permission.objects.get_or_create(
                    name=f'Can {permiso} {self.nombre}',
                    content_type=ContentType.objects.get_for_model(Rol),
                    codename=f'{permiso}_{self.nombre}'
                ))
            if creado:
                for permisos in permiso_nuevo:
                    nuevo_grupo.permissions.add(permisos[0].id)
                    super().save(*args, **kwargs)               
        else:
            rol_antiguo = Rol.objects.filter(id = self.id_rol).values('nombre').first()
            if rol_antiguo['nombre'] == self.nombre:
                super().save(*args, **kwargs)
            else:
                Group.objects.filter(name= rol_antiguo['nombre']).update(name=f'{self.nombre}')
                for permiso in permisos_defecto:
                    Permission.objects.filter(codename= f"{permiso}_{rol_antiguo['nombre']}").update(
                        codename=f'{permiso}_{self.nombre}',
                        name=f'Can {permiso} {self.nombre}'
                    )
                super().save(*args,**kwargs)



class Persona(models.Model):
    cedula_ciudadano = models.PositiveIntegerField('Cedula de ciudadanía', default=None)
    nombres = models.CharField('Nombres', max_length=30)
    apellidos = models.CharField('Apellidos', max_length=50)
    edad = models.DateField(blank=True, null=True)
    telefono = models.IntegerField('Telefono', blank=True, null=True)
    imagen = models.ImageField(upload_to='institucional', default=None, null=True)
    semestre = models.ForeignKey("institucional.Semestre", on_delete=models.CASCADE, blank=True, null=True)
    creditos_aprobados_semestre = models.IntegerField(blank=True, null=True, default=0)
    codigo_universitario = models.IntegerField('Codigo universitario', unique=True, blank=True, null=True)


    REQUIRED_FIELDS = ['nombres', 'apellidos', 'cedula_ciudadano']

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class UsuarioActivoManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario',unique =True, max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    persona = models.ForeignKey(Persona, default=None, on_delete=models.CASCADE, blank=True, null=True)
    rol = models.ForeignKey(Rol, default=None, on_delete=models.CASCADE, blank=True, null=True)
    objects = UsuarioManager()
    activo = UsuarioActivoManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def save(self, *args, **kwargs):
        if not self.id:
            if self.rol is not None:
                grupo = Group.objects.filter(name__iexact=self.rol.nombre).first()
                if grupo is not None:
                    self.groups.add(grupo)
                    super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        else:
            if self.rol is not None:
                grupo_antiguo = Usuario.objects.filter(id=self.id).values('rol__nombre').first()
                if grupo_antiguo['rol__nombre'] == self.rol.nombre:
                    grupo = Group.objects.filter(name=grupo_antiguo['rol__nombre']).first()
                    if grupo is not None:
                        self.groups.add(grupo.id)
                else:
                    grupo_anterior = Group.objects.filter(name=grupo_antiguo['rol__nombre']).first()
                    if grupo_anterior is not None:
                        self.groups.remove(grupo_anterior)
                    nuevo_grupo = Group.objects.filter(name=self.rol.nombre).first()
                    if nuevo_grupo is not None:
                        self.groups.add(nuevo_grupo)
                    super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)

    def __str__(self):
        return self.username