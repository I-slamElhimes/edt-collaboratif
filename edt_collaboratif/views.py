from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def dashboard(request):
    from events.models import Evenement
    from groups.models import Groupe, Invitation
    from notifications.models import Notification

    today = datetime.date.today()
    context = {
        'evenements_aujourd_hui': Evenement.objects.filter(
            createur=request.user, date=today
        ).order_by('heure_debut'),
        'prochains_evenements': Evenement.objects.filter(
            createur=request.user, date__gte=today
        ).order_by('date', 'heure_debut')[:5],
        'mes_groupes': request.user.groupes_rejoints.all()[:5],
        'invitations_en_attente': Invitation.objects.filter(
            destinataire=request.user, statut='EN_ATTENTE'
        ),
        'notifications_recentes': Notification.objects.filter(
            destinataire=request.user, lu=False
        )[:5],
    }
    return render(request, 'dashboard.html', context)