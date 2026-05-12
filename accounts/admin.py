from django.contrib import admin
from .models import ProfilUtilisateur

@admin.register(ProfilUtilisateur)
class ProfilAdmin(admin.ModelAdmin):
    # Ce qu'on voit dans la liste
    list_display = ('user', 'tentatives_connexion', 'compte_bloque')
    # Les filtres à droite
    list_filter = ('compte_bloque',)
    # La recherche
    search_fields = ('user__username',)
    
    # Action personnalisée pour débloquer en 1 clic
    actions = ['debloquer']

    def debloquer(self, request, queryset):
        queryset.update(compte_bloque=False, tentatives_connexion=0)
        self.message_user(request, "Les comptes sélectionnés ont été débloqués.")
    debloquer.short_description = "Débloquer les utilisateurs"