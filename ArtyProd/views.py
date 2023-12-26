
from imaplib import _Authenticator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import *
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Personnel,  Projet, Service, Equipe



from django.shortcuts import render
from django.core.mail import send_mail

def ListPersonnel(request):
    personnel_list = Personnel.objects.all()
    context = {'personnel_list': personnel_list}
    return render(request, 'artyprod/home.html', context)
def ListService(request):
        services= Service.objects.all()
        context={'services':services}
        return render( request,'artyprod/home.html',context )


class ContactUsView(TemplateView):
    template_name = 'artyprod/home.html'
    def post(self, request, *args, **kwargs):
        # Process the form data and send the email
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        sender_email = request.POST.get('email')
        recipient_email = 'artyprod2024@gmail.com'
        subject = request.POST.get('subject')
        message = f" Name: {name}\n\n  Message: {request.POST.get('message')}"

        send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)

        # Redirect back to the same page after form submission
        return self.render_to_response(self.get_context_data())

contact_us = ContactUsView.as_view()

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import ClientRegistrationForm

def client_register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('indexA')
    else:
        form = ClientRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

def client_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return render(request,'artyprod/layout.html' )
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def client_logout(request):
    logout(request)
    return redirect('indexA')


def TEST(request):
         return render(request,'artyprod/base.html' )

def indexA(request):
         return render(request,'artyprod/home.html' )

def portfoliodetails(request):
     return render(request,'artyprod/portfolio-details.html' )

from django.shortcuts import render
from .models import DemandeProjet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DemandeProjet

from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.message import EmailMessage


@login_required
def demande_projet(request):
    client = None
    if hasattr(request.user, 'client'):
        client = request.user.client
    if request.method == 'POST':
        # Get the form data
        nom_projet = request.POST.get('nom_projet')
        description = request.POST.get('description')
        
        if client:
            # Create a new project request
            DemandeProjet.objects.create(nom_projet=nom_projet, description=description, client=client)
            
            # Send email notification to the client
            subject = 'Nouvelle demande de projet'
            message = f"Cher {client.nom},\n\nVotre demande de projet a été soumise avec succès. Nous vous contacterons bientôt.\n\nCordialement,\nL'équipe de notre site"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [client.user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            
            # Display a success message to the user
            context = {'success': True}
            return render(request, 'clients/demande_projet.html', context)
        else:
            # Handle the case where the user has no related client object
            context = {'error': 'User has no related client object'}
            return render(request, 'clients/demande_projet.html', context)
    else:
        demandes_projet = []
        if client:
            # Get all project requests for the current client
            demandes_projet = DemandeProjet.objects.filter(client=client)
        
        context = {'demandes_projet': demandes_projet}
        return render(request, 'clients/demande_projet.html', context)









from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Projet

@login_required
def myprojects_view(request):
    # Récupérer l'utilisateur actuel
    client = request.user.client
    projets = Projet.objects.filter(clients=client)
    context = {'projets': projets, 'client': client}
    return render(request, 'clients/myproject.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ClientUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        client_form = ClientUpdateForm(request.POST, request.FILES, instance=request.user.client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            context = {'success': True}
            return render(request, 'clients/edit_profile.html', context)
    else:
        user_form = UserUpdateForm(instance=request.user)
        client_form = ClientUpdateForm(instance=request.user.client)
    
    context = {'user_form': user_form, 'client_form': client_form}
    return render(request, 'clients/edit_profile.html', context)

@login_required
def client_profile(request):
    client = request.user.client
    context = {'client': client}
    return render(request, 'clients/client_profile.html', context)



def indexHome(request):
     return render(request,'artyprod/index.html' )

def AffichageProjet(request):
    projets = Projet.objects.all()
    context = {'projets': projets}
    return render(request, 'clients/projets.html', context)









from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import  BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog/blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        comment = Comment(user=user, content=content, blog=post)
        comment.save()
        return redirect('blogs_comments', slug=slug)

    return render(request, "blog/blog_comments.html", {'post': post, 'comments': comments})



def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "blog/search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "blog/search.html", {})

# views.py

def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == "POST":
        content = request.POST.get('content', '')
        comment.content = content
        comment.save()
        return redirect('blogs_comments', slug=comment.blog.slug)
    
    return render(request, 'blog/edit_comment.html', {'comment': comment})


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == "POST":
        blog_slug = comment.blog.slug
        comment.delete()
        return redirect('blogs_comments', slug=blog_slug)
    
    return render(request, 'blog/delete_comment.html', {'comment': comment})




