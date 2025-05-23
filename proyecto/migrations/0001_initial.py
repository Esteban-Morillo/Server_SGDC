# Generated by Django 5.1.4 on 2025-05-07 04:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_contrato', models.CharField(default='', max_length=100)),
                ('nombres', models.CharField(default='', max_length=100)),
                ('apellidos', models.CharField(default='', max_length=100)),
                ('tipo_documento', models.CharField(choices=[('CC', 'Cedula'), ('NIT', 'Nit')], default='', max_length=30)),
                ('identificacion', models.CharField(default='', max_length=20)),
                ('fecha_de_transaccion', models.DateField(blank=True, null=True)),
                ('lugar_de_expedicion', models.CharField(default='', max_length=100)),
                ('telefono', models.CharField(default='', max_length=20)),
                ('banco', models.CharField(choices=[('BC', 'Bancolombia'), ('NE', 'Nequi'), ('DA', 'Daviplata')], default='', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datecompleted', models.DateTimeField(blank=True, null=True)),
                ('importante', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
