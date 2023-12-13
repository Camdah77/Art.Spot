from django.shortcuts import render, redirect, get_object_or_404
from .models import Artwork  
from .forms import AddArtworkForm
from django.http import HttpResponse
from django.template import loader

# HTML- pages
def landing_page(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'index.html')  

def blog(request):
    return render(request, 'blogg/blog.html')  

def events(request):
    return render(request, 'events/upcoming.html')  

def market(request):
    return render(request, 'artworks/artworks.html')   

def about(request):
    return render(request, 'about/aboutartspot.html')  

def login(request):
    return render(request, '/account/login.html')  

def logout(request):
    return render(request, '/account/logout.html')  

def signup(request):
    return render(request, 'account/signup.html')  

# List uploaded Artworks
def get_artwork(request):
    artworks = Artwork.objects.all()
    context = {
        'artworks': artworks  
    }

    return render(request, 'artworks/artworks.html', context)

# Add artworks
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

# Edit artworks
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

# Delete artworks 
def delete_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()
    return redirect('get_artwork')