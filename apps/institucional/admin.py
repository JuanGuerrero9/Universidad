from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.institucional.models import *

class AsignaturaResource(resources.ModelResource):
    class Meta:
        model = Asignatura

class AsignaturaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['nombre']
    resource_class = AsignaturaResource




# Register your models here.
admin.site.register(Facultad)
admin.site.register(Programa)
admin.site.register(PlanEstudio)
admin.site.register(Semestre)
admin.site.register(PagoRecibo)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(AsignaturaUsuario)
admin.site.register(HorarioAsignatura)
admin.site.register(DiaSemana)
admin.site.register(Bancos)
admin.site.register(TarjetaCredito)
