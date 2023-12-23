from django.contrib import admin
from django.urls import path, include
from artspot.views import (
    landing_page, add_artwork, edit_artwork, delete_artwork, PostList, custom_login, LogoutView, 
    PostDetail, home, blog, events, market, registration, about, Post_like)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'artspot'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('add/', add_artwork, name='add_artwork'),
    path('edit/<artwork_id>/', edit_artwork, name='edit'),
    path('delete/<artwork_id>/', delete_artwork, name='delete'),
    path('about/', about, name='about'),
    path('events/', events, name='events'),
    path('market/', market, name='market'),
    path('blog/', PostList.as_view(), name='blog'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', registration, name='register'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('', home, name='home'),
  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)