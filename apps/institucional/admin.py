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

class AntecesoraResource(resources.ModelResource):
    class Meta:
        model = Antecesora

class AntecesoraAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AntecesoraResource

class AsignaturaAntecesoraResource(resources.ModelResource):
    class Meta:
        model = AsignaturaAntecesora
        import_id_fields = ['id_asignatura_antecesora']

class AsignaturaAntecesoraAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AsignaturaAntecesoraResource




# Register your models here.
admin.site.register(Facultad)
admin.site.register(Programa)
admin.site.register(PlanEstudio)
admin.site.register(Semestre)
admin.site.register(PagoRecibo)
admin.site.register(AsignaturaAntecesora, AsignaturaAntecesoraAdmin)
admin.site.register(NotaFinal)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(AsignaturaUsuario)
admin.site.register(Cortes)
admin.site.register(Antecesora, AntecesoraAdmin)
admin.site.register(HorarioAsignatura)
admin.site.register(DiaSemana)
admin.site.register(Bancos)
admin.site.register(TarjetaCredito)
