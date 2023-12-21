from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Artwork, Post, Comment, Product, Profile, Category
from .forms import AddArtworkForm, CommentForm, SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
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
def signout(request):
    return render(request, 'members/logout.html')
def UserRegisterView(request):
    return render(request, 'members/register.html')  
def profile(request):
    return render(request, 'members/profile.html')  

  # Member Login/Logout
def signout(request):
    return render(request, 'members/logout.html')

def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')  # Adjust the URL as needed.
        else:
            # Return an 'invalid login' error message.
            return render(request, 'members/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'members/login.html')

  # ArtMarket Product

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'artworks/product.html', {'product': product})

#Artmarket category
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
  
# User Profile 
class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'members/signup.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'members/editprofile.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'instagram_url', ]
    success_url = reverse_lazy('home')

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'members/profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')

def password_success(request):
    return render(request, 'members/password_sussess.html')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'members/editprofile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

#Blog

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blogg/blog.html"
    paginate_by = 6

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

class Post_like(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('artspot:post_detail', args=[slug]))

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


# members/Signup.html
class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'members/register.html'
    success_url = reverse_lazy('login')
    
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




