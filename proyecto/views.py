from django.shortcuts import render, redirect, get_object_or_404
# Libreria para creacion de formulario de registro
from django.contrib.auth.forms import UserCreationForm
# Libreria para iniciar sesion
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # libreria para registrar usuarios
from django.contrib.auth import login, logout
# Libreria para autentificar el iniciar sesion
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .forms import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#Librerias generar documento 
from docxtpl import DocxTemplate
from mailmerge import MailMerge
import os
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now
# Libreria para visualizar el docuemrento en la pagina web
from docx2pdf import convert


# Create your views here.
# Vista de la pagina home
def home(request):
    return render(request, 'home.html')

# Vista de la pagina de registro de usuarios
def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })

    else:
        # comparar que las contraseñas concidan
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Si coinciden se realiza el registro de usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # Guarda el registro del usuario en la base de datos
                login(request, user)
                # Redirecciona o ingresa a la pagina principal
                return redirect('principal')

            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error": 'el usuario ya existe!'
                })
        return render(request, 'registro.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden!'
        })

# Vista de la pagina principal
@login_required
def principal(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'principal.html', {'tasks': tasks})

# Vista de la pagina contratos finalizados
@login_required
def contrato_fin(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'principal.html', {'tasks': tasks})

# Vista para crear formulario
@login_required
def crearformulario(request):
    if request.method == 'GET':
        return render(request, 'crearformulario.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            New_task = form.save(commit=False)
            New_task.user = request.user
            New_task.save()

            # 1. Cargar plantilla desde documentos/plantilla.docx
            doc = DocxTemplate(os.path.join(settings.BASE_DIR, "documentos", "plantilla.docx"))

            # 2. Preparar contexto
            contexto = {
                'nombre_del_contrato': New_task.nombre_del_contrato,
                'nombres': New_task.nombres,
                'apellidos': New_task.apellidos,
                'tipo_documento': New_task.tipo_documento,
                'identificacion': New_task.identificacion,
                'fecha_de_transaccion': New_task.fecha_de_transaccion.strftime('%Y-%m-%d') if New_task.fecha_de_transaccion else 'Fecha no disponible',
                'lugar_de_expedicion': New_task.lugar_de_expedicion,
                'telefono': New_task.telefono if New_task.telefono else 'No disponible',
                'banco': New_task.banco,
                'importante': 'Sí' if New_task.importante else 'No'
            }

            # 3. Generar y guardar el archivo Word
            output_dir = os.path.join(settings.BASE_DIR, "documentos")
            output_dir = os.path.join(settings.MEDIA_ROOT, "contratos")
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"contrato_{New_task.id}.docx")
            output_path = os.path.join(settings.BASE_DIR, "documentos", f"contrato_{New_task.id}.docx")

            doc.render(contexto)
            doc.save(output_path)

            # Convertir a PDF
            pdf_output_path = os.path.join(output_dir, f"contrato_{New_task.id}.pdf")
            convert(output_path, pdf_output_path)

            # Redirigir a vista del PDF
            return redirect('ver_documento', documento_id=New_task.id)

            # return redirect('principal')

        except ValueError:
            return render(request, 'crearformulario.html', {
                'form': TaskForm,
                'error': 'Por favor proporsione un dato valido'
            })

# Vista de contratos abiertos o en proceso
@login_required
def informes(request, informes_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=informes_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'informes.html', {'task': task, 'form': form})
    else:
        try:
            # Obtener la tarea existente
            task = get_object_or_404(Task, pk=informes_id, user=request.user)
            form = TaskForm(request.POST, instance=task)

            # Guardar los nuevos datos del formulario
            form.save()

            # Actualizar el documento Word con los nuevos datos
            doc = DocxTemplate(os.path.join(settings.BASE_DIR, "documentos", "plantilla.docx"))

            # Preparar los nuevos datos que serán reemplazados en el Word
            contexto = {
                'nombre_del_contrato': task.nombre_del_contrato,
                'nombres': task.nombres,
                'apellidos': task.apellidos,
                'tipo_documento': task.tipo_documento,
                'identificacion': task.identificacion,
                'fecha_de_transaccion': task.fecha_de_transaccion.strftime('%Y-%m-%d'),
                'lugar_de_expedicion': task.lugar_de_expedicion,
                'telefono': task.telefono,
                'banco': task.banco,
                'importante': 'Sí' if task.importante else 'No'
            }

            # Ruta para guardar el archivo actualizado
            output_dir = os.path.join(settings.BASE_DIR, "documentos")
            os.makedirs(output_dir, exist_ok=True)

            # Guardar el documento actualizado
            output_path = os.path.join(output_dir, f"contrato_{task.id}.docx")
            doc.render(contexto)
            doc.save(output_path)

            return redirect('principal')

        except ValueError:
            return render(request, 'informes.html', {
                'task': task, 
                'form': form, 
                'error': 'Error al actualizar datos de contrato'
            })

# Pagina de contratos finalizados o cerrados
@login_required
def tarea_realizada(request, informes_id):
    task = get_object_or_404(Task, pk=informes_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('principal')

# Vista para visualizar documento
@login_required
def ver_documento(request, documento_id):
    pdf_url = settings.MEDIA_URL + f'contratos/contrato_{documento_id}.pdf'
    pdf_path = os.path.join(settings.MEDIA_ROOT, f'contratos/contrato_{documento_id}.pdf')
    
    if not os.path.exists(pdf_path):
        return render(request, 'error.html', {'message': 'El archivo PDF no existe.'})
    
    return render(request, 'ver_documento.html', {'pdf_url': pdf_url})

# Pagina de contratos finalizados o cerrados
@login_required
def tarea_eliminada(request, informes_id):
    task = get_object_or_404(Task, pk=informes_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('principal')

# Vista de cerrar sesión
@login_required
def salir(request):
        logout(request)
        return redirect('home')

# Vista de inicio de sesión.
def iniciar(request):
    if request.method == 'GET':
        return render(request, 'iniciar.html', {
     'form': AuthenticationForm
      })
    else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST
                ['password'])

            if user is None:
                return render(request, 'iniciar.html', {
         'form': AuthenticationForm,
          'error': 'Usuario o Contraseña incorrecto'
           })

            else:
                login(request, user)
            return redirect('principal')