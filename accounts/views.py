from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ProfilForm
from .models import ProfilUtilisateur

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé ! Tu peux te connecter.")
            return redirect('accounts:connexion')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})

def connexion_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # 1. On cherche d'abord l'utilisateur pour vérifier s'il est bloqué
        from django.contrib.auth.models import User
        try:
            target_user = User.objects.get(username=u)
            # On récupère ou on crée le profil s'il n'existe pas (sécurité)
            profil, created = ProfilUtilisateur.objects.get_or_create(user=target_user)
            
            if profil.compte_bloque:
                messages.error(request, "Compte bloqué (3 échecs). Contacte l'admin.")
                return render(request, 'accounts/connexion.html')
        except User.DoesNotExist:
            profil = None

        # 2. Tentative d'authentification
        user = authenticate(username=u, password=p)
        
        if user:
            # On s'assure encore une fois que le profil existe pour cet utilisateur
            profil, created = ProfilUtilisateur.objects.get_or_create(user=user)
            profil.tentatives_connexion = 0
            profil.save()
            
            login(request, user)
            return redirect('dashboard')
        else:
            # Échec : on augmente le compteur si l'utilisateur existe
            if profil:
                profil.tentatives_connexion += 1
                if profil.tentatives_connexion >= 3:
                    profil.compte_bloque = True
                profil.save()
                messages.warning(request, f"Identifiants invalides. Échec {profil.tentatives_connexion}/3")
            else:
                messages.error(request, "Utilisateur introuvable.")
    
    return render(request, 'accounts/connexion.html')
@login_required

def profil_view(request):
    if request.method == 'POST':
        # On passe request.FILES pour l'avatar !
        form = ProfilForm(request.POST, request.FILES, instance=request.user.profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour !")
            return redirect('accounts:profil')
    else:
        form = ProfilForm(instance=request.user.profil)
    
    return render(request, 'accounts/profil.html', {'form': form})

def deconnexion_view(request):
    logout(request)
    return redirect('accounts:connexion')