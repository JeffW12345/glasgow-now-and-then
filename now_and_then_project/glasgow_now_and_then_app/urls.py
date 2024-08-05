from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from . import views

app_name = 'nowandthen'

urlpatterns = ([
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('photo_feed/', views.photo_feed, name='photo_feed'),
    path('add_picture/', views.add_picture, name='add_picture'),
    path('era/<str:era>/', views.era_search_results, name='era_search_results'),
    path('search/', views.search_results, name='search_results'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
])