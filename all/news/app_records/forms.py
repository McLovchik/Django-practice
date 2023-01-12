from django import forms
from .models import Record, RecordImage
from django.forms import ClearableFileInput


class RecordModelForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['text']


class RecordImageModelForm(forms.ModelForm):
    class Meta:
        model = RecordImage
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }


class UploadRecordForm(forms.Form):
    file = forms.FileField()
