"""
URL configuration for SGDC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from proyecto import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path de aplicacion registro
    path('', views.home, name = 'home'),
    # Path para redireccionar luego de registrarse
    path('registro/', views.registro, name = 'registro'),
    # Path para redireccionar a la pagina de principal
    path('principal/', views.principal, name = 'principal'),
    # Path para redireccionar a la pagina de contratos completados
    path('contrato_fin/', views.contrato_fin, name = 'contrato_fin'),
    # Path para redireccionar al formulario de creacion de contratos
    path('principal/crearformulario/', views.crearformulario, name = 'crearformulario'),
    # Path para redireccionar a la lista de informes creados
    path('principal/<int:informes_id>/', views.informes, name = 'informes'),
    # Path para marcar o definir contratos como finalizados
    path('principal/<int:informes_id>/realizado', views.tarea_realizada, name = 'tarea_realizada'),
    # Path para eliminar contratos
    path('principal/<int:informes_id>/eliminar', views.tarea_eliminada, name = 'tarea_eliminada'),
    # Path para redireccionar luego cerrar sesión
    path('salir/', views.salir, name = 'salir'),
    # Path para redireccionar luego iniciar sesión
    path('iniciar/', views.iniciar, name = 'iniciar'),
    # Path para visualizar documento
    path('ver_documento/<int:documento_id>/', views.ver_documento, name='ver_documento'),
    path('principal/', views.principal, name='principal'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
