from django import forms
from .models import Artwork, Comment
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#LOGIN# authentication/forms.py

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

#SIGNUP
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Artist name')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.CharField(max_length=30, label='Email')
    password1 = forms.CharField(max_length=30, label='Choose a password')  
    password2 = forms.CharField(max_length=30, label='Type your password again please') 
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # Override the save method if needed
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


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

