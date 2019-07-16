from django import forms

from .models import Image


class ImageForm(forms.Form):
    url = forms.CharField(label='Image url', required=True)
    language = forms.ChoiceField(choices=Image.languages, required=True)
    enforce_process = forms.BooleanField(required=False)
