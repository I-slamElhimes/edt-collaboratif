import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Groupe, Invitation

# Import notifications si l'app existe, sinon on ignore
try:
    from notifications.utils import creer_notification
except ImportError:
    def creer_notification(**kwargs):
        pass

@login_required
def liste_groupes(request):
    groupes = request.user.groupes_rejoints.all()
    return render(request, 'groups/liste.html', {'groupes': groupes})

@login_required
def creer_groupe(request):
    from django import forms
    class GroupeForm(forms.ModelForm):
        class Meta:
            model = Groupe
            fields = ['nom', 'description']

    form = GroupeForm(request.POST or None)
    if form.is_valid():
        groupe = form.save(commit=False)
        groupe.proprietaire = request.user
        groupe.save()
        groupe.membres.add(request.user)
        messages.success(request, f"Groupe créé ! Code : {groupe.code_acces}")
        return redirect('groups:detail', pk=groupe.pk)
    return render(request, 'groups/creer.html', {'form': form})

@login_required
def rejoindre_groupe(request):
    from django import forms
    class RejoindreForm(forms.Form):
        code_acces = forms.CharField(max_length=12, label="Code d'accès")

    form = RejoindreForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data['code_acces'].upper()
        try:
            groupe = Groupe.objects.get(code_acces=code)
            groupe.membres.add(request.user)
            messages.success(request, f"Tu as rejoint le groupe {groupe.nom} !")
            return redirect('groups:detail', pk=groupe.pk)
        except Groupe.DoesNotExist:
            messages.error(request, "Code incorrect. Vérifie avec le créateur du groupe.")
    return render(request, 'groups/rejoindre.html', {'form': form})

@login_required
def detail_groupe(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    return render(request, 'groups/detail.html', {'groupe': groupe})

@login_required
def inviter_utilisateur(request, groupe_pk):
    from django import forms
    class InviterForm(forms.Form):
        email = forms.EmailField(label="Email de l'utilisateur à inviter")

    groupe = get_object_or_404(Groupe, pk=groupe_pk)
    form = InviterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        try:
            destinataire = User.objects.get(email=email)
            inv, created = Invitation.objects.get_or_create(
                groupe=groupe,
                destinataire=destinataire,
                defaults={'expediteur': request.user}
            )
            if created:
                creer_notification(
                    destinataire=destinataire,
                    type_notif='INVITATION',
                    titre=f"Invitation au groupe {groupe.nom}",
                    message=f"{request.user.username} t'invite dans {groupe.nom}",
                    lien="/groups/invitations/"
                )
                messages.success(request, f"Invitation envoyée à {email} !")
            else:
                messages.info(request, "Une invitation a déjà été envoyée à cet utilisateur.")
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur avec cet email.")
    return render(request, 'groups/inviter.html', {'form': form, 'groupe': groupe})

@login_required
def mes_invitations(request):
    invitations = Invitation.objects.filter(destinataire=request.user, statut='EN_ATTENTE')
    return render(request, 'groups/invitations.html', {'invitations': invitations})

@login_required
def accepter_invitation(request, inv_pk):
    inv = get_object_or_404(Invitation, pk=inv_pk, destinataire=request.user)
    inv.statut = 'ACCEPTEE'
    inv.date_reponse = datetime.datetime.now()
    inv.save()
    inv.groupe.membres.add(request.user)
    creer_notification(
        destinataire=inv.expediteur,
        type_notif='ACCEPTATION',
        titre=f"{request.user.username} a accepté ton invitation",
        message=f"Il a rejoint le groupe {inv.groupe.nom}",
        lien=f"/groups/{inv.groupe.pk}/"
    )
    messages.success(request, f"Tu as rejoint {inv.groupe.nom} !")
    return redirect('groups:liste')

@login_required
def refuser_invitation(request, inv_pk):
    inv = get_object_or_404(Invitation, pk=inv_pk, destinataire=request.user)
    inv.statut = 'REFUSEE'
    inv.date_reponse = datetime.datetime.now()
    inv.save()
    messages.info(request, "Invitation refusée.")
    return redirect('groups:invitations')

@login_required
def disponibilites_groupe(request, groupe_pk):
    groupe = get_object_or_404(Groupe, pk=groupe_pk)
    membres = groupe.membres.all()
    date_cible = datetime.date.today()
    evenements_par_membre = {
        m.username: list(m.evenements_crees.filter(date=date_cible).values('heure_debut', 'heure_fin'))
        for m in membres
    }
    return render(request, 'groups/disponibilites.html', {
        'groupe': groupe,
        'date': date_cible,
        'evenements_par_membre': evenements_par_membre
    })