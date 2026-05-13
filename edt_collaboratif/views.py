from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
# On importe les modèles ici pour que ce soit plus propre
from events.models import Evenement
from groups.models import Groupe, Invitation
from notifications.models import Notification

def home(request):
    """Page d'accueil pour les visiteurs non connectés."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    context = {
        'hide_navbar': True,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    today = datetime.date.today()
    
    # 1. Événements d'aujourd'hui (pour le compteur du haut)
    evts_today = Evenement.objects.filter(
        createur=request.user, 
        date=today
    ).order_by('heure_debut')

    # 2. Prochains événements (pour la liste centrale)
    # On prend aujourd'hui ET le futur
    prochains = Evenement.objects.filter(
        createur=request.user, 
        date__gte=today
    ).order_by('date', 'heure_debut')[:5]

    # 3. Invitations (Important pour le badge orange)
    invites = Invitation.objects.filter(
        destinataire=request.user, 
        statut='EN_ATTENTE'
    )

    # 4. Groupes (On utilise "membres" car c'est un ManyToManyField)
    # Tu es membre de ces groupes
    groupes = request.user.groupes_rejoints.all()[:5]

    # 5. Notifications
    notifs = Notification.objects.filter(
        destinataire=request.user, 
        lu=False
    ).order_by('-created_at')[:5]

    context = {
        'evenements_aujourd_hui': evts_today,
        'prochains_evenements': prochains,
        'mes_groupes': groupes,
        'invitations_en_attente': invites,
        'notifications_recentes': notifs,
    }
    
    return render(request, 'dashboard.html', context)