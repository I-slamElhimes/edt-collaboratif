import uuid
from django.db import models
from django.contrib.auth.models import User

class Groupe(models.Model):
    nom          = models.CharField(max_length=150)
    description  = models.TextField(blank=True, default='')
    code_acces   = models.CharField(max_length=12, unique=True, blank=True)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupes_crees')
    membres      = models.ManyToManyField(User, related_name='groupes_rejoints', blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_acces:
            self.code_acces = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Groupe : {self.nom}"

    class Meta:
        verbose_name = "Groupe"


class Invitation(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE',   'Acceptée'),
        ('REFUSEE',    'Refusée'),
    ]
    groupe       = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='invitations')
    expediteur   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_envoyees')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_recues')
    statut       = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_envoi   = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(null=True, blank=True)
    message      = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Invitation {self.destinataire} → {self.groupe.nom} ({self.statut})"

    class Meta:
        unique_together = ['groupe', 'destinataire']
        verbose_name    = "Invitation"