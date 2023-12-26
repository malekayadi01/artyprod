from datetime import datetime
from email.headerregistry import Group
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.html import format_html




class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    skill = models.CharField(max_length=255, blank=True)

    ficher = models.FileField(upload_to='media/', blank=True)
    Img = models.ImageField(upload_to='media/', blank=True)
    lien_linkedIn = models.URLField(blank=True)

    def __str__(self):
        return f'{self.nom}'

    def has_perm(self, perm, obj=None):
        if perm == 'view_equipe' and obj is not None:
            return obj.membres.filter(id=self.id).exists()
        return super().has_perm(perm, obj)

    def image_tag(self):
        if self.Img:
            return format_html('<img src="{}" width="100"/>'.format(self.Img.url))
        else:
            return '-'

    image_tag.short_description = 'Image'


class Service(models.Model):
    TYPE_CHOICES = (
        ('Product Design', 'Product Design'),
        ('UX UI Design', 'UX UI Design'),
        ('Branding', 'Branding'),
        ('Digital Strategy', 'Digital Strategy'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    Img = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f'{self.type}, {self.description}'


class Equipe(models.Model):
    nom = models.CharField(max_length=255)
    membres = models.ManyToManyField(Personnel)
   
    def __str__(self):
        return f'{self.nom}'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, default="")
    adresse = models.CharField(max_length=255, default="")
    telephone = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    Img = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}, {self.adresse}, {self.telephone}'


from django.core.validators import MaxValueValidator, MinValueValidator

class Projet(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    acheve = models.BooleanField(default=False)
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    details = models.FileField(upload_to='media/', null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.libelle}, {self.description}, {self.date_debut}, {self.date_fin}'


class GalerieProjet(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    media = models.FileField(upload_to='media/', null=True, blank=True)
    legende = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.legende if self.legende else self.media.name
    

class Tache(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    membre = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.description} '





from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Personnel, Client

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Personnel').exists():
            Personnel.objects.create(user=instance)
        elif instance.groups.filter(name='Client').exists():
            Client.objects.create(user=instance)





class DemandeProjet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    nom_projet = models.CharField(max_length=255)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    TYPE_CHOICES = (
        ('En_attente', 'En_attente'),
        ('Acceptée', 'Acceptée'),
        ('Rejetée', 'Rejetée')
    )
    statut = models.CharField(max_length=50, choices=TYPE_CHOICES, default='En_attente')
   
    def __str__(self):
        return f"{self.nom_projet} ({self.client})"

















from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now



class BlogPost(models.Model):
    title=models.CharField(max_length=255)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.CharField(max_length=130)
    content=models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    
    def get_absolute_url(self):
        return reverse('blogs')
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    

