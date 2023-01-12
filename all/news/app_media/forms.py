from django import forms
from .models import File


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=64)
    file = forms.FileField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'file')


class MultiFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
