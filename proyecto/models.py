from django.db import models
from django.contrib.auth.models import User  # libreria para registrar usuarios
from django.conf import settings



# Create your models here.
class Task(models.Model):
    
    TIPO_DOCUMENTO = [
        ('CC', 'Cedula'),
        ('NIT', 'Nit'),
    ]

    BANCO = [
        ('Bancolombia', 'Bancolombia'),
        ('Nequi', 'Nequi'),
        ('Daviplata', 'Daviplata'),
    ]


    nombre_del_contrato = models.CharField(max_length=100, default='')
    nombres = models.CharField(max_length=100, default='')
    apellidos = models.CharField(max_length=100, default='')
    tipo_documento = models.CharField(max_length=30, choices=TIPO_DOCUMENTO, default='')
    identificacion = models.CharField(max_length=20, default='')
    fecha_de_transaccion = models.DateField(null=True, blank=True)
    lugar_de_expedicion = models.CharField(max_length=100, default='')
    telefono =  models.CharField(max_length=20, default='')
    banco = models.CharField(max_length=30, choices=BANCO, default='')
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) 
    importante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_del_contrato + ' - by ' + self.nombres + ' ' + self.apellidos 

