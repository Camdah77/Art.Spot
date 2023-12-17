"""pp4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pp4/urls.py

from django.contrib import admin
from django.urls import path, include
from artspot.views import (
    landing_page, get_artwork, add_artwork, edit_artwork, delete_artwork,
    home, about, blog, events, market, login, logout, signup, PostList, PostDetail, PostLike, account_profile
)
from artspot import views as pp4_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from members.views import UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This is for the empty path
    path('get_artwork/', pp4_views.get_artwork, name='get_artwork'),
    path('add/', pp4_views.add_artwork, name='add_artwork'),
    path('edit/<artwork_id>/', pp4_views.edit_artwork, name='edit'),
    path('delete/<artwork_id>/', pp4_views.delete_artwork, name='delete'),
    path('about/', about, name='about'),
    path('events/', events, name='events'),
    path('market/', market, name='market'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('summernote/', include('django_summernote.urls')),
    path('profile/', account_profile, name='account_profile'),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('blog/', PostList.as_view(), name='blog'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', PostLike.as_view(), name='post_like'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
