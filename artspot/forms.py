from django import forms
from .models import Artwork, Comment, NewUser
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Layout, Fieldset, Submit

#LOGIN# authentication/forms.py

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

#SIGNUP
class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
        model = NewUser
        fields = ['username', 'email', 'password1', 'password2']

    
# Marketplace
class AddArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['name', 'artist', 'length', 'width', 'category', 'medium', 'price' ]
  # Additional validation, if needed
    def clean_length(self):
        length = self.cleaned_data.get('length')
        if length is not None and length <= 0:
            raise forms.ValidationError("Length must be a positive integer.")
        return length 
    def clean_width(self):
        width = self.cleaned_data.get('width')
        if width is not None and width <= 0:
            raise forms.ValidationError("Width must be a positive integer.")
        return width
# Blog
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)