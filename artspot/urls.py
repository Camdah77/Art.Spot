from django.urls import path, include
from members.views import UserRegisterView

urlpatterns = [
   path('members/', include('django.contrib.auth.urls')),
   path('members/', include('members.urls')),
]