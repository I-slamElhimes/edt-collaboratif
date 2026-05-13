from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('',                     views.calendrier_view,     name='calendrier'),
    path('liste/',               views.liste_evenements,    name='liste'),
    path('creer/',               views.creer_evenement,     name='creer'),
    path('<int:pk>/',           views.detail_evenement,    name='detail'),
    path('<int:pk>/modifier/',  views.modifier_evenement,  name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_evenement, name='supprimer'),
    path('<int:pk>/partager/',  views.partager_evenement,  name='partager'),
]