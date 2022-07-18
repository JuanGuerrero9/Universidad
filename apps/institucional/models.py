from django.db import models
from apps.usuario.models import Usuario, Persona


class ModeloAbstracto(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField('Fecha de Creación', auto_now_add=True, auto_now=False)
    fecha_modificacion = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

class Facultad(ModeloAbstracto):
    nombre = models.CharField('Nombre de Facultad', max_length=50)
    director = models.CharField('Nombre de Director', max_length=50)
    telefono = models.IntegerField('Telefono de Facultad', default=None)
    email = models.EmailField('Correo de contacto')

    def __str__(self):
        return self.nombre
    

class Programa(ModeloAbstracto):
    nombre = models.CharField('Nombre del programa', max_length=50)
    cantidad_semestres = models.SmallIntegerField('Semestres que tiene el programa', default=1)
    telefono = models.IntegerField('Telefono', default=None)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class PlanEstudio(ModeloAbstracto):
    nombre = models.CharField('Nombre del plan de estudio', max_length=50, default=0)
    total_creditos = models.IntegerField('Creditos del programa', default=None)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre

class Semestre(ModeloAbstracto):
    nombre = models.CharField(max_length=50)
    numero_semestre = models.IntegerField(unique=True)
    creditos_permitidos = models.IntegerField('Creditos permitidos', default = None)
    plan_estudio = models.ForeignKey(PlanEstudio, on_delete=models.CASCADE, null=True, blank=True, default=None)
    costo = models.IntegerField('Precio del semestre', default=None)

    def __str__(self):
        return self.nombre

class PagoRecibo(ModeloAbstracto):
    codigo = models.IntegerField(default=None, unique=True)
    esta_pago = models.BooleanField(default=False)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.codigo)


class Asignatura(ModeloAbstracto):
    nombre = models.CharField('Nombre de Asignatura', max_length=80)
    creditos = models.IntegerField('Creditos', default=None)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, blank=True)
    antecesora = models.ForeignKey("self", on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.nombre


class DiaSemana(ModeloAbstracto):
    nombre_dia = models.CharField('Nombre Dia de la semana', max_length=40, blank=True)

    def __str__(self):
        return self.nombre_dia


class HorarioAsignatura(ModeloAbstracto):
    hora_inicio = models.TimeField(blank=True)
    hora_final = models.TimeField(blank=True, default=None)
    dia_semana = models.ForeignKey(DiaSemana, on_delete=models.CASCADE, blank=True, default=None, null=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, blank=True)
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.asignatura}'

class AsignaturaUsuario(ModeloAbstracto):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)
    aprobado = models.BooleanField(default=False)
    matricula_realizada = models.BooleanField(default=False)
    horario_asignatura = models.ForeignKey(HorarioAsignatura, on_delete=models.CASCADE, default=None, null=True, blank=True)
    nota_corte1 = models.IntegerField(default=0, blank=True)
    nota1_agregada = models.BooleanField(default=False)
    nota_corte2 = models.IntegerField(default=0, blank=True)
    nota2_agregada = models.BooleanField(default=False)
    nota_corte3 = models.IntegerField(default=0, blank=True)
    nota3_agregada = models.BooleanField(default=False)
    porcentaje_corte1_y_2 = models.IntegerField(default=30, editable=False)
    porcentaje_corte3 = models.IntegerField(default=40, editable=False)
    nota_final = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.usuario.username} {self.asignatura}'


class Bancos(ModeloAbstracto):
    nombre_banco = models.CharField('Nombre del banco', max_length=70)

    def __str__(self):
        return self.nombre_banco

class TarjetaCredito(ModeloAbstracto):
    numero_tarjeta = models.BigIntegerField(default=0)
    saldo = models.IntegerField(default=0)
    banco = models.ForeignKey(Bancos, on_delete=models.CASCADE, default=None)
    codigo_seguridad = models.IntegerField(default=0)
    credito_maximo = models.IntegerField(default=0)
    propietario = models.CharField('Nombre del propietario', max_length=70)
    esta_embargada = models.BooleanField(default=False)   

    def __str__(self):
        return self.propietario