from django.contrib import admin
from django.urls import path, include
from artspot.views import (
    landing_page, add_artwork, edit_artwork, delete_artwork, PostList, custom_login, logout, register,
    PostDetail, home, blog, events, market, about, Post_like, welcome)
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
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register/members/welcome/', welcome, name='welcome'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('members/', include('allauth.urls')),
    path('', home, name='home'),
  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
