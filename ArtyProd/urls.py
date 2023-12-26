
from .views import *
from django.urls import path
from django.conf.urls.static import static as statistics
from django.conf import settings
from django.contrib.auth import views as auth_views

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import client_register
from . import views


urlpatterns = [

    path('Personnel/',ListPersonnel, name='ListPersonnel'),
    path('Service/',ListService, name='ListService'),
    path("blogs/", views.blogs, name="blogs"),
    path("blogs/blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path('blogs/blog/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('blogs/blog/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
  
    path("search/", views.search, name="search"),
    
    path('client-profile/', client_profile, name='client_profile'),

    path('AffichageProjet/', AffichageProjet,name='AffichageProjet'),
    path('indexHome/', indexHome, name='indexHome'),
    path('login/', views.client_login, name='client_login'),
    path('logout/', views.client_logout, name='client_logout'),
    path('register/', client_register, name='register'),
    path('demande_projet/', demande_projet, name='demande_projet'),
    path('', indexA, name='indexA'),
    path('TEST/', TEST, name='TEST'),
    path('portfoliodetails/', portfoliodetails, name='portfoliodetails'),

    path('myprojects/', myprojects_view, name='myprojects'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('contact/', ContactUsView.as_view(), name='contact'),
 

]+ statistics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)