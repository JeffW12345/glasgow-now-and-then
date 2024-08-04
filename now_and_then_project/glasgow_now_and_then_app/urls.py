from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'nowandthen'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('photo_feed/', views.photo_feed, name='photo_feed'),
    path('add_picture/', views.photo_feed, name='add_picture'),
    path('1970/', views.photo70, name='1970'),
    path('1980/', views.photo80, name='1980'),
    path('2010/', views.photo10, name='2010'),
    path('search/', views.search_results, name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
