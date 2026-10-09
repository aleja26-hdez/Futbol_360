from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'escuela', 'password1', 'password2']


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'escuela', 'is_active']

class NotificacionForm(forms.Form):
    destinatario = forms.ModelChoiceField(queryset=Usuario.objects.filter(rol='padre'), label="Enviar a")
    titulo = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)
