from django.contrib.auth.views import LogoutView
from django.views.generic.edit import CreateView
from django.contrib import admin
from django.urls import path, include
from artspot.views import (
    landing_page, add_artwork, edit_artwork, delete_artwork, PostLike, PostList, PostDetail, custom_login, 
    home, about, blog, events, market, UserRegisterView, UserEditView, PasswordsChangeView, 
    ShowProfilePageView, EditProfilePageView, CreateProfilePageView, password_success)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from artspot import views

app_name = 'artspot'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', add_artwork, name='add_artwork'),
    path('edit/<artwork_id>/', edit_artwork, name='edit'),
    path('delete/<artwork_id>/', delete_artwork, name='delete'),
    path('about/', about, name='about'),
    path('events/', events, name='events'),
    path('market/', market, name='market'),
    path('blog/', PostList.as_view(), name='blog'),
    path('accounts/', include('allauth.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='members/password_change.html'), name='password_change'),
    path('password_success', password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)