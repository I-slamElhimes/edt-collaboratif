from django.test import TestCase
from django.contrib.auth.models import User
from .models import Groupe, Invitation

class GroupeModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass', email='alice@test.com')
        self.user2 = User.objects.create_user(username='bob',   password='pass', email='bob@test.com')

    def test_code_acces_genere_automatiquement(self):
        groupe = Groupe.objects.create(nom='TestGroupe', proprietaire=self.user1)
        self.assertIsNotNone(groupe.code_acces)
        self.assertEqual(len(groupe.code_acces), 8)

    def test_code_acces_unique(self):
        g1 = Groupe.objects.create(nom='G1', proprietaire=self.user1)
        g2 = Groupe.objects.create(nom='G2', proprietaire=self.user2)
        self.assertNotEqual(g1.code_acces, g2.code_acces)

    def test_invitation_statut_defaut(self):
        groupe = Groupe.objects.create(nom='G1', proprietaire=self.user1)
        inv = Invitation.objects.create(
            groupe=groupe,
            expediteur=self.user1,
            destinataire=self.user2
        )
        self.assertEqual(inv.statut, 'EN_ATTENTE')

    def test_invitation_unique_par_groupe_et_destinataire(self):
        from django.db import IntegrityError
        groupe = Groupe.objects.create(nom='G1', proprietaire=self.user1)
        Invitation.objects.create(groupe=groupe, expediteur=self.user1, destinataire=self.user2)
        with self.assertRaises(Exception):
            Invitation.objects.create(groupe=groupe, expediteur=self.user1, destinataire=self.user2)