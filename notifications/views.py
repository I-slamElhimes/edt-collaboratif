

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def liste_notifications(request):
    notifs = Notification.objects.filter(
        destinataire=request.user
    ).order_by('lu', '-created_at')
    return render(request, 'notifications/liste.html', {'notifications': notifs})

@login_required
def marquer_lu(request, pk):
    notif = get_object_or_404(Notification, pk=pk, destinataire=request.user)
    notif.lu = True
    notif.save()
    return redirect(notif.lien or 'notifications:liste')

@login_required
def tout_marquer_lu(request):
    Notification.objects.filter(
        destinataire=request.user, 
        lu=False
    ).update(lu=True)
    return redirect('notifications:liste')