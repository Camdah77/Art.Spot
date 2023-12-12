from django import forms
from .models import Artwork

class AddArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['name', 'artist', 'category', 'medium', 'price',]

   