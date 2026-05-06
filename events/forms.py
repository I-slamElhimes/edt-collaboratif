from django import forms
from .models import Evenement

class EvenementForm(forms.ModelForm):
    date        = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    heure_debut = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    heure_fin   = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model  = Evenement
        fields = ['titre', 'description', 'date', 'heure_debut', 'heure_fin',
                  'type_evt', 'lieu', 'priorite', 'couleur', 'est_prive']

    def clean(self):
        data  = super().clean()
        debut = data.get('heure_debut')
        fin   = data.get('heure_fin')
        if debut and fin and fin <= debut:
            raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")
        return data