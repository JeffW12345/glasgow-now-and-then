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
    path('add_picture/', views.add_picture, name='add_picture'),
    path('era/<str:era>/', views.era_search_results, name='era_search_results'),
    path('search/', views.search_results, name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
