from django import forms

from .models import Inplace

# formulario para categorias
class InplaceForm(forms.ModelForm):
    class Meta:
        model = Inplace
        fields = ['datetime_insitu','img','latitude','longitude','product']
        
        widget = {'latitude': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})