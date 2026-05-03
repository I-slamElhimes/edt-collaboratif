from django.contrib import admin
from .models import Groupe, Invitation

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'proprietaire', 'code_acces', 'created_at']
    search_fields = ['nom', 'proprietaire__username']

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['groupe', 'expediteur', 'destinataire', 'statut']
    list_filter  = ['statut']