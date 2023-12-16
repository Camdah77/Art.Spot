from artspot.views  import PostList, PostDetail, PostLike
from django.urls import path, include
from members.views import UserRegisterView

urlpatterns = [
   path('', PostList.as_view(), name='blog'),
   path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
   path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
   path('members/', include('django.contrib.auth.urls')),
   path('members/', include('members.urls')),
]