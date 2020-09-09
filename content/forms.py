from django import forms

from .models import Video, Drive_urls

# formulario para categorias
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name','description','state','img','video','start_date','end_date','duration','contract']
        
        widget = {'name': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})



class DriveForm(forms.ModelForm):
    class Meta:
        model = Drive_urls
        fields = ['city','info','url','state']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})