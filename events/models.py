from django.db import models
from django.contrib.auth.models import User

class Evenement(models.Model):
    PRIORITE_CHOICES = [
        ('HAUTE',   'Haute'),
        ('MOYENNE', 'Moyenne'),
        ('BASSE',   'Basse'),
    ]
    TYPE_CHOICES = [
        ('COURS',     'Cours'),
        ('REUNION',   'Réunion'),
        ('EXAMEN',    'Examen'),
        ('PERSONNEL', 'Personnel'),
        ('AUTRE',     'Autre'),
    ]

    titre        = models.CharField(max_length=200)
    description  = models.TextField(blank=True, default='')
    date         = models.DateField()
    heure_debut  = models.TimeField()
    heure_fin    = models.TimeField()
    type_evt     = models.CharField(max_length=20, choices=TYPE_CHOICES, default='AUTRE')
    lieu         = models.CharField(max_length=200, blank=True, default='')
    priorite     = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='MOYENNE')
    est_prive    = models.BooleanField(default=False)
    couleur      = models.CharField(max_length=7, default='#3b82f6')
    createur     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evenements_crees')
    participants = models.ManyToManyField(User, related_name='evenements_participes', blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} — {self.date}"

    def check_conflit(self, user):
        return Evenement.objects.filter(
            createur=user,
            date=self.date,
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        ).exclude(pk=self.pk).exists()

    class Meta:
        ordering     = ['date', 'heure_debut']
        verbose_name = "Événement"