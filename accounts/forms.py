from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur
from django.core.exceptions import ValidationError

class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription étendu pour inclure l'email et les noms."""
    email = forms.EmailField(required=True, label="Adresse Email")
    first_name = forms.CharField(max_length=100, required=True, label="Prénom")
    last_name = forms.CharField(max_length=100, required=True, label="Nom")

    class Meta(UserCreationForm.Meta):
        model = User
        # On définit les champs qui seront affichés dans l'ordre
        fields = ("username", "email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Règle : doit contenir @emsi.ma
        if not email.endswith('@emsi.ma') and not email.endswith('@gmail.com'):
            raise ValidationError("Veuillez utiliser votre adresse email institutionnelle (@emsi.ma).")
        return email


class ProfilForm(forms.ModelForm):
    """Formulaire pour mettre à jour la bio et l'avatar du profil."""
    class Meta:
        model = ProfilUtilisateur
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Parlez-nous de vous (études, passions, objectifs...)'
            }),
        }


class ConnexionForm(forms.Form):
    """Formulaire de connexion simple (utilisé dans ta vue de connexion)."""
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: manale_nadir'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )