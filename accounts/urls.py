from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_request, name="profile"),
    path('', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate'),
]
