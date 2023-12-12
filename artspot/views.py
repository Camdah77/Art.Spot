from django.shortcuts import render
from .models import Artwork  # Use a different name for the model class, e.g., Artwork

def get_artwork(request):
    artworks = Artwork.objects.all()
    context = {
        'artworks': artworks  # Fix the variable name here
    }

    return render(request, 'artspot/artworks/artworks.html', context)