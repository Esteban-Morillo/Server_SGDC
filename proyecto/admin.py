from django.contrib import admin
from.models import Task

# Clase para mostrar la fecha de creacion del documento
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Registrar mi modelo
admin.site.register(Task, TaskAdmin)