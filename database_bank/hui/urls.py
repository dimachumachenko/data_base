from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.home, name="index"),
    path('home/', views.home , name='home'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    #path('profile/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login')

    ]