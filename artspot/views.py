from django.shortcuts import render, redirect
from .models import Artwork  
from .forms import AddArtworkForm

def get_artwork(request):
    artworks = Artwork.objects.all()
    context = {
        'artworks': artworks  # Fix the variable name here
    }

    return render(request, 'artworks/artworks.html', context)

def add_artwork(request):
    if request.method == 'POST':
        form = AddArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('get_artwork')
    else:
        form = AddArtworkForm()

    context = {
        'form': form
    }
    return render(request, 'artworks/add_artwork.html', context)