from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta: 
        model = Task
        fields = ['nombre_del_contrato', 'nombres', 'apellidos', 'tipo_documento', 'identificacion', 'fecha_de_transaccion', 'lugar_de_expedicion',
                  'telefono', 'banco', 'importante']
        widgets = {
            'nombre_del_contrato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre del contrato'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba sus nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba sus apellidos'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de identificación'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}),
            'fecha_de_transaccion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lugar_de_expedicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar de expedición'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}),
            'banco': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione banco'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input mx-5'}),

        }