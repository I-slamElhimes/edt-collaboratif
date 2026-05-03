from django.contrib import admin
from .models import Evenement

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display   = ['titre', 'date', 'heure_debut', 'priorite', 'createur']
    list_filter    = ['priorite', 'type_evt', 'date']
    search_fields  = ['titre', 'createur__username']
    date_hierarchy = 'date'