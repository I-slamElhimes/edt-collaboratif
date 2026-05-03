from django.contrib import admin
from .models import ProfilUtilisateur

@admin.register(ProfilUtilisateur)
class ProfilAdmin(admin.ModelAdmin):
    list_display  = ['user', 'compte_bloque', 'tentatives_connexion']
    search_fields = ['user__username']