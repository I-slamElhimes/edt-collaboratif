def nb_notifications(request):
    if request.user.is_authenticated:
        from .models import Notification
        count = Notification.objects.filter(
            destinataire=request.user, 
            lu=False
        ).count()
        return {'nb_notifs_non_lues': count}
    return {'nb_notifs_non_lues': 0}