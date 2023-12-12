from django import forms
from .models import Artwork


class AddartworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['name', 'artist', 'category', 'medium',  'price']