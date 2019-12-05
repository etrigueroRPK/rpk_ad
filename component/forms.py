from django import forms

from .models import Category, Location

# formulario para categorias
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description','state','img']
        labels = {'name':'Nombre de la categoria','state':'Estado'}
        widget = {'name': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

# formulario para locations

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'state','img','start_date', 'end_date', 'address']
        
        widget = {'name': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
    