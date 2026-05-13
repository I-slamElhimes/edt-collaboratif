from django.urls import path, reverse_lazy # Importe reverse_lazy ici
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('profil/', views.profil_view, name='profil'),
    
    # MODIFICATION ICI : On ajoute success_url
    path('modifier-mdp/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/modifier_mdp.html',
        success_url=reverse_lazy('accounts:password_change_done') # On lui dit d'aller vers la route avec le préfixe accounts
    ), name='modifier_mdp'),
    
    path('mdp-modifie/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/mdp_ok.html'
    ), name='password_change_done'),
]