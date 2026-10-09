from django import forms
from .models import Escuela, FotoInstalacion

class EscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = ['nombre', 'ciudad', 'direccion', 'edad_minima', 'edad_maxima', 'telefono', 'instagram', 'facebook', 'logo']


class FotoInstalacionForm(forms.ModelForm):
    class Meta:
        model = FotoInstalacion
        fields = ['imagen', 'descripcion']