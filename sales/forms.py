from django import forms

from .models import Client, Contract

# formulario para categorias
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','description','state','img']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['start_date','end_date','description','state','client']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})