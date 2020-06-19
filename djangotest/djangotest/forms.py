from .models import fileupload
from django import forms
import datetime

class fileuploadForm(forms.ModelForm):
    class Meta:
        model = fileupload
        fields = ("__all__")
