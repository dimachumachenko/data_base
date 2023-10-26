from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import NewsListView
from .views import NewsListView, NewsFeed

app_name = 'mybankapp'

urlpatterns = [
    path('', views.home, name='home'),
    # path('search/', views.search, name='search'),
    path('profile/<str:currency>', views.profile, name='profile'),
    path('login/', views.temp_login, name='login'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login')
    #
    path('registration/', views.temp_register, name='registration'),
    path('logout', views.temp_logout, name='logout'),
    # path('db/', views.DBViewer., name='db')
    path('request_credit/<str:currency>', views.request_credit, name='request_credit'),
    path('pay_off/<str:currency>', views.pay_off_credit, name='pay_off_credit'),
    path('tmp/', views.tmp, name='tmp'),
    path('search/', views.search, name='search'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('feed/', NewsFeed(), name='news-feed'),

    ]