from django import views
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import include
import path
from django.conf.urls.static import static

from ArtyProd import settings


urlpatterns = [
path('admin/', admin.site.urls),
path('ArtyProd/', include('ArtyProd.urls')),
path('', views.home,name='home'),
path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)