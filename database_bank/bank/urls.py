from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



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
    path('news/', views.make_rss, name='news_list'),
    path('add_news/', views.create_news, name='create_news'),
    path('xml/', views.data_as_xml, name='xml'),
    path('add_rss/', views.add_rss, name='add_rss'),
    ]