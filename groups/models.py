import random
import string
from django.db import models
from django.contrib.auth.models import User

def generer_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupes_crees')
    membres = models.ManyToManyField(User, related_name='groupes_rejoints', blank=True)
    code_acces = models.CharField(max_length=12, unique=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_acces:
            code = generer_code()
            while Groupe.objects.filter(code_acces=code).exists():
                code = generer_code()
            self.code_acces = code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Invitation(models.Model):
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
    ]
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='invitations')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_envoyees')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_recues')
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('groupe', 'destinataire')

    def __str__(self):
        return f"Invitation de {self.expediteur} → {self.destinataire} pour {self.groupe}"