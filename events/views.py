from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evenement
from .forms import EvenementForm
import datetime, calendar

@login_required
def calendrier_view(request):
    annee = int(request.GET.get('annee', datetime.date.today().year))
    mois  = int(request.GET.get('mois',  datetime.date.today().month))
    cal   = calendar.monthcalendar(annee, mois)
    evenements = Evenement.objects.filter(
        createur=request.user,
        date__year=annee,
        date__month=mois
    )
    return render(request, 'events/calendrier.html', {
        'calendrier': cal,
        'evenements': evenements,
        'annee': annee,
        'mois': mois,
        'mois_nom': calendar.month_name[mois],
    })

@login_required
def liste_evenements(request):
    evenements = Evenement.objects.filter(createur=request.user)
    return render(request, 'events/liste.html', {'evenements': evenements})

@login_required
def creer_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evt = form.save(commit=False)
            evt.createur = request.user
            if evt.check_conflit(request.user):
                messages.warning(request, "Conflit d'horaire détecté avec un autre événement !")
            evt.save()
            messages.success(request, "Événement créé !")
            return redirect('events:calendrier')
    else:
        form = EvenementForm()
    return render(request, 'events/creer.html', {'form': form})

@login_required
def detail_evenement(request, pk):
    evt = get_object_or_404(Evenement, pk=pk, createur=request.user)
    return render(request, 'events/detail.html', {'evt': evt})

@login_required
def modifier_evenement(request, pk):
    evt = get_object_or_404(Evenement, pk=pk, createur=request.user)
    form = EvenementForm(request.POST or None, instance=evt)
    if form.is_valid():
        form.save()
        messages.success(request, "Événement modifié !")
        return redirect('events:detail', pk=pk)
    return render(request, 'events/modifier.html', {'form': form, 'evt': evt})

@login_required
def supprimer_evenement(request, pk):
    evt = get_object_or_404(Evenement, pk=pk, createur=request.user)
    if request.method == 'POST':
        evt.delete()
        messages.success(request, "Événement supprimé.")
        return redirect('events:calendrier')
    return render(request, 'events/supprimer_confirm.html', {'evt': evt})

@login_required
def partager_evenement(request, pk):
    evt = get_object_or_404(Evenement, pk=pk, createur=request.user)
    return render(request, 'events/partager.html', {'evt': evt})