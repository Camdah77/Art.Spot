from django.shortcuts import render
from .models import Artwork  # Use a different name for the model class, e.g., Artwork

def get_artwork(request):
    try:
        artwork_instance = Artwork.objects.get(id=1)
    except Artwork.DoesNotExist:
        artwork_instance = None

    return render(request, 'artspot/index.html', {'artwork': artwork_instance})
