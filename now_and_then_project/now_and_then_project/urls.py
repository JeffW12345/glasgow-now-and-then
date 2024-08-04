from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('glasgow_now_and_then_app.urls')),
    path('admin/', admin.site.urls),
]