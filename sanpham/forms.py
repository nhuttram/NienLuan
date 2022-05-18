from django import forms

class uploadMulti(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))