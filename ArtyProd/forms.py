from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Personnel, Projet, Service, Equipe


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'


class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
from django import forms

class ContactForm(forms.Form):
    sender = forms.EmailField(label='Votre adresse email')
    subject = forms.CharField(label='Sujet', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)




class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    email = forms.EmailField(label='Adresse e-mail')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    nom = forms.CharField(max_length=255, required=True)
    adresse = forms.CharField(max_length=255, required=True)
    telephone = forms.CharField(max_length=255, required=True)
    Img = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        if commit:
            user.save()
        client = Client(user=user)
        client.save()
        return user


from django import forms
from .models import Client

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'adresse','email' ,'telephone', 'Img']

from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]
        


from django import forms
from .models import  BlogPost

        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content of the Blog'}),
        }