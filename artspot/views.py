from django.shortcuts import render, redirect, get_object_or_404
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
        form = AddArtworkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_artwork')
    else:
        form = AddArtworkForm()

    context = {
        'form': form
    }
    return render(request, 'artworks/add_artwork.html', context)

def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        form = AddArtworkForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('get_artwork')
    form = AddArtworkForm(instance=artwork)
    context = {
        'form': form
    }
    return render(request, 'artworks/edit_artwork.html', context)

def delete_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()
    return redirect('get_artwork')