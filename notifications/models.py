from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    TYPE_CHOICES = [
        ('INVITATION',  'Invitation reçue'),
        ('ACCEPTATION', 'Invitation acceptée'),
        ('PARTAGE',     'Événement partagé'),
        ('RAPPEL',      'Rappel événement'),
        ('INFO',        'Information'),
    ]
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type_notif   = models.CharField(max_length=15, choices=TYPE_CHOICES, default='INFO')
    titre        = models.CharField(max_length=200)
    message      = models.TextField()
    lien         = models.CharField(max_length=300, blank=True, default='')
    lu           = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.type_notif}] {self.titre} → {self.destinataire.username}"

    class Meta:
        ordering     = ['-created_at']
        verbose_name = "Notification"