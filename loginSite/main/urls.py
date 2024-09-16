from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name="home" ),
    path('home', views.home, name="home" ),
    path('sign_up', views.sign_up, name="sign_up" ),
    path('new_post', views.new_post, name="new_post"),
    path('profile', views.profile, name='profile'),
]
