from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Artwork, Post, Comment, NewUser
from .forms import LoginForm, NewUserForm, AddArtworkForm, CommentForm
from django.contrib.auth.forms import UserCreationForm

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
def custom_login(request):
    return render(request, 'members/login.html')
def logout(request):
    return render(request, 'members/logout.html')
def UserRegisterView(request):
    return render(request, 'members/register.html')  
def profile(request):
    return render(request, 'members/profile.html')  
def welcome(request):
    return render(request, 'members/welcome.html')


# members/login.html
def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome. We wish you a creative day!")
            return redirect('home')
        else:
            messages.success(request, "Please try again")
            return redirect('members/login.html')
    
    else:
        return render(request, 'members/login.html', {})

# members/register.html
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            # Process the valid form (e.g., save user) and redirect
            # This part is missing in your code
            return redirect('members/welcome.html')
        else:
            # If the form is not valid, you can handle it here
            print(form.errors)
    else:
        form = NewUserForm()

    context = {'form': form}
    return render(request, 'members/register.html', context)
            
# members/logout.html
def logout(request):
     return render(request, 'members/logout.html')
     return render(request, 'members/login.html')


# artmarket/products
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'artworks/product.html', {'product': product})
def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'artworks/category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')
  
class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        print(f"Slug value: {slug}")  # Add this line
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

    
# Artmarket 
def market(request):
    products = Product.objects.all()
    return render(request, 'artworks/artworks.html', {'products':products})
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
    template_name = "blogg/blog.html"
    paginate_by = 6
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
class Post_like(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('artspot:post_detail', args=[slug]))