from django.contrib import admin
from .models import Groupe, Invitation

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'proprietaire', 'code_acces', 'date_creation']
    readonly_fields = ['code_acces']

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['groupe', 'expediteur', 'destinataire', 'statut', 'date_envoi']