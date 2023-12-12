from django.shortcuts import render, redirect
from .models import Artwork  
from .forms import AddartworkForm

def get_artwork(request):
    artworks = Artwork.objects.all()
    context = {
        'artworks': artworks  # Fix the variable name here
    }

    return render(request, 'artworks/artworks.html', context)

def add_artwork(request):
        if request.method == 'POST':
            form = AddartworkForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('get_artwork')
        form = AddartworkForm()
        context = {
            'form': form
        }
        return render(request, 'artworks/add_artwork.html')