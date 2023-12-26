from django import forms
from django.contrib import admin
from.models import *

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Projet
from django.contrib import admin
from .models import Projet

from django.contrib import admin
from .models import Equipe

class TacheInline(admin.TabularInline):
    model = Tache
    extra = 1
from django import forms
from .models import Tache

class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = [ 'description']

class EquipeForm(forms.ModelForm):
    taches = forms.inlineformset_factory(Equipe, Tache, form=TacheForm, extra=1)

    class Meta:
        model = Equipe
        fields = ['nom']

class EquipeAdmin(admin.ModelAdmin):
    form = EquipeForm
    inlines = [TacheInline]

    filter_horizontal = ('membres',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(membres__user=request.user)

admin.site.register(Equipe, EquipeAdmin)

from django.contrib import admin


admin.site.register(Service)
from django.contrib import admin
from django.utils.html import format_html
from .models import Client, Personnel


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.Img:
            return format_html('<img src="{}" width="100"/>'.format(obj.Img.url))
        else:
            return '-'
    image_tag.short_description = 'Image'



from django.contrib.auth.admin import UserAdmin

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'skill', 'lien_linkedIn', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.Img:
            return format_html('<img src="{}" width="100"/>'.format(obj.Img.url))
        else:
            return '-'
    image_tag.short_description = 'Image'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Client, ClientAdmin)
admin.site.register(Personnel, PersonnelAdmin)




from django.contrib import admin
from.models import *

# Register your models here.
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q

from .models import Projet, Equipe


class PersonnelChangeList(ChangeList):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Personnel').exists():
            qs = qs.filter(Q(equipe__membres=request.user.personnel) | Q(clients=request.user.client))
        return qs

class ImageInline(admin.TabularInline):
    model = GalerieProjet
    extra = 0

class ProjetAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'date_debut', 'date_fin', 'acheve', 'equipe')
    list_filter = ('equipe', 'clients', 'acheve')
    search_fields = ('libelle', 'description')
    inlines = [ImageInline]
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Personnel').exists():
            return qs.filter(equipe__membres=request.user.personnel)
        elif request.user.groups.filter(name='Client').exists():
            return qs.filter(clients=request.user.client)
        else:
            return qs.none()  # aucun projet si utilisateur non autorisé

admin.site.register(Projet, ProjetAdmin)
from django.contrib import admin






from .models import Equipe, Client, Projet, GalerieProjet

from django.utils.safestring import mark_safe


class GalerieProjetAdmin(admin.ModelAdmin):
    list_display = ('projet', 'legende', 'media_preview')
    list_filter = ('projet',)

    def media_preview(self, obj):
        if obj.media:
            return mark_safe('<img src="{url}" width="100"/>'.format(url=obj.media.url))
        else:
            return 'Aucune media'

    media_preview.short_description = 'Aperçu'

    fieldsets = (
        ('Informations sur le projet', {
            'fields': ('projet',)
        }),
        ('Media', {
            'fields': ('media', 'legende'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        else:
            equipe = user.personnel.equipe_set.first()
            return qs.filter(projet__equipe=equipe)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "projet":
            if not request.user.is_superuser:
                # Filtrer les projets selon l'équipe à laquelle l'utilisateur est affecté
                kwargs["queryset"] = Projet.objects.filter(equipe__membres__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(GalerieProjet, GalerieProjetAdmin)

admin.site.register(DemandeProjet)



admin.site.register(BlogPost)
admin.site.register(Comment)