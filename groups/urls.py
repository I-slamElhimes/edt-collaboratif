from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',                                  views.liste_groupes,        name='liste'),
    path('creer/',                            views.creer_groupe,          name='creer'),
    path('rejoindre/',                        views.rejoindre_groupe,      name='rejoindre'),
    path('invitations/',                      views.mes_invitations,       name='invitations'),
    path('<int:pk>/',                         views.detail_groupe,         name='detail'),
    path('<int:groupe_pk>/inviter/',          views.inviter_utilisateur,   name='inviter'),
    path('<int:groupe_pk>/dispo/',            views.disponibilites_groupe, name='disponibilites'),
    path('invitation/<int:inv_pk>/accepter/', views.accepter_invitation,   name='accepter'),
    path('invitation/<int:inv_pk>/refuser/',  views.refuser_invitation,    name='refuser'),
]