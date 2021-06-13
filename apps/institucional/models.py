from django.db.models.signals import post_save
from django.db import models
from apps.usuario.models import Usuario, Persona


class Facultad(models.Model):
    id_facultad = models.AutoField(primary_key =True )
    nombre      = models.CharField('Nombre de Facultad', max_length= 50)
    director    = models.CharField('Nombre de Director', max_length=50)
    telefono    = models.IntegerField('Telefono de Facultad', default= None)
    email       = models.EmailField('Correo de contacto')

    def __str__(self):
        return self.nombre
    

class Programa(models.Model):
    id_programa        = models.AutoField(primary_key = True)
    nombre             = models.CharField('Nombre del programa', max_length = 50)
    cantidad_semestres = models.SmallIntegerField('Semestres que tiene el programa', default = 1)
    telefono           = models.IntegerField('Telefono', default = None)
    facultad           = models.ForeignKey(Facultad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class PlanEstudio(models.Model):
    id_plan_estudio = models.AutoField(primary_key = True)
    nombre          = models.CharField('Nombre del plan de estudio', max_length = 50, default=0)
    total_creditos  = models.IntegerField('Creditos del programa', default = None)
    programa        = models.ForeignKey(Programa, on_delete= models.CASCADE)

    def __str__(self):
        return self.nombre

class Semestre(models.Model):
    id_semestre         = models.AutoField(primary_key = True)
    nombre              = models.CharField(max_length= 50)
    creditos_permitidos = models.IntegerField('Creditos permitidos', default = None)
    plan_estudio        = models.ForeignKey(PlanEstudio, on_delete= models.CASCADE)
    costo               = models.IntegerField('Precio del semestre', default= None)

    def __str__(self):
        return self.nombre

class PagoRecibo(models.Model):
    id_pago_recibo         = models.AutoField(primary_key = True)
    codigo                 = models.IntegerField(default= None, unique=True)
    esta_pago              = models.BooleanField(default = False)
    semestre               = models.ForeignKey(Semestre, on_delete= models.CASCADE)
    persona                = models.ForeignKey(Persona, on_delete= models.CASCADE, null= True, blank= True)

    def __str__(self):
        return str(self.codigo)


class Asignatura(models.Model):
    id_asignatura          = models.AutoField(primary_key = True)
    nombre                 = models.CharField('Nombre de Asignatura', max_length= 30)
    creditos               = models.IntegerField('Creditos', default= None)
    semestre               = models.ForeignKey(Semestre, on_delete= models.CASCADE, blank=True)

    def __str__(self):
        return self.nombre

class Antecesora(models.Model):
    id_antecesora = models.AutoField(primary_key = True)
    asignatura    = models.ForeignKey(Asignatura, on_delete= models.CASCADE, blank= True, default= None)

    def __str__(self):
        return self.asignatura.nombre

class AsignaturaAntecesora(models.Model):
    id_asignatura_antecesora = models.AutoField(primary_key = True)
    asignatura               = models.ForeignKey(Asignatura, on_delete= models.CASCADE, blank= True, default=None)
    antecesora               = models.ForeignKey(Antecesora, on_delete= models.CASCADE, blank= True, default=None, null=True)

    def __str__(self):
        return self.asignatura.nombre

class DiaSemana(models.Model):
    id_dia_semana = models.AutoField(primary_key= True)
    nombre_dia    = models.CharField('Nombre Dia de la semana', max_length=40, blank= True)

    def __str__(self):
        return self.nombre_dia


class HorarioAsignatura(models.Model):
    id_horario          = models.AutoField(primary_key= True)
    hora_inicio         = models.TimeField(blank= True)
    hora_final          = models.TimeField(blank= True, default= None)
    dia_semana          = models.ForeignKey(DiaSemana, on_delete= models.CASCADE, blank= True, default= None, null= True)
    Asignatura          = models.ForeignKey(Asignatura, on_delete= models.CASCADE, blank= True)
    docente             = models.ForeignKey(Usuario, on_delete= models.CASCADE, blank= True)

    def __str__(self):
        return self.Asignatura.nombre

class AsignaturaUsuario(models.Model):
    id_asignatura_usuario       = models.AutoField(primary_key=True)
    usuario                     = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    asignatura                  = models.ForeignKey(Asignatura, on_delete= models.CASCADE)
    activo                      = models.BooleanField(default= False)
    aprobado                    = models.BooleanField(default= False)
    matricula_realizada         = models.BooleanField(default= False)
    horario_asignatura          = models.ForeignKey(HorarioAsignatura, on_delete= models.CASCADE, default=None, null= True)

    def __str__(self):
        return self.usuario

class Cortes(models.Model):
    id_cortes                   = models.AutoField(primary_key= True)
    nota_corte1                 = models.IntegerField(default=0)
    nota_corte2                 = models.IntegerField(default=0)
    nota_corte3                 = models.IntegerField(default=0)
    porcentaje_corte1_y_2       = models.IntegerField(default=0.30, editable= False)
    porcentaje_corte3           = models.IntegerField(default=0.40, editable= False)
    asignatura_usuario          = models.ForeignKey(AsignaturaUsuario, on_delete= models.CASCADE, null=True)

    def __str__(self):
        return self.asignatura_usuario

class NotaFinal(models.Model):
    id_nota_final       = models.AutoField(primary_key= True)
    cortes              = models.ForeignKey(Cortes, on_delete= models.CASCADE, null= True)
    nota                = models.IntegerField(default=0)
    asignatura          = models.ForeignKey(AsignaturaUsuario, on_delete= models.CASCADE, null=True)

    def __str__(self):
        return self.asignatura.nombre


