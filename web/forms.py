from django import forms


class ImageForm(forms.Form):
    url = forms.CharField(label='Image url')
