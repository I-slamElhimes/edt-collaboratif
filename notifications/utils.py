from .models import Notification

def creer_notification(destinataire, type_notif, titre, message, lien=''):

    return Notification.objects.create(
        destinataire=destinataire,
        type_notif=type_notif,
        titre=titre,
        message=message,
        lien=lien
    )