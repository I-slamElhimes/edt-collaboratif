from django.db import models
from django.contrib.auth.models import User

class ProfilUtilisateur(models.Model):
    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    bio                  = models.TextField(blank=True, default='')
    avatar               = models.ImageField(upload_to='avatars/', blank=True, null=True)
    tentatives_connexion = models.IntegerField(default=0)
    compte_bloque        = models.BooleanField(default=False)
    date_creation        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

    class Meta:
        verbose_name = "Profil Utilisateur"