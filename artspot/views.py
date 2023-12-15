from django.shortcuts import render, redirect, get_object_or_404
from .models import Artwork, Post, Comment, Profile
from .forms import AddArtworkForm, CommentForm, CustomUserCreationForm 
from django.http import HttpResponse
from django.template import loader
from django.views import generic, View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
def profile(request):
    return render(request, 'account/profile.html')  


# Register /signup
def signup_view(request):
    form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required # Require user logged in before they can access profile page
def account_profile(request):
    return render(request, 'account/profile.html')


# MARKETPLACE 
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

#BLOG
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'blogg/blog.html'
    paginate_by = 6
class PostDetail(DetailView):
    model = View
    template_name = 'blogg/post_detail.html'  
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blogg/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blogg/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )
class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))