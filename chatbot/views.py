import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .utils import get_chatbot_response
from .models import MessageChatbot
from django.shortcuts import render

@login_required
def chatbot_page(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('message', '').strip()
            if not message:
                return JsonResponse({'reply': 'Écris ta question !'})
            reponse = get_chatbot_response(message, request.user)
            MessageChatbot.objects.create(
                utilisateur=request.user,
                question=message,
                reponse=reponse
            )
            return JsonResponse({'reply': reponse})
        except Exception as e:
            return JsonResponse({'reply': "Désolé, une erreur s'est produite. Réessaie."})

    # GET → afficher la page
    messages = MessageChatbot.objects.filter(
        utilisateur=request.user
    ).order_by('created_at')[:20]
    return render(request, 'chatbot/chat.html', {'messages': messages})
@require_POST
def chatbot_view(request):
    try:
        message = request.POST.get('message', '').strip()
        if not message:
            return JsonResponse({'reply': 'Écris ta question !'})

        reponse = get_chatbot_response(message, request.user)

        MessageChatbot.objects.create(
            utilisateur=request.user,
            question=message,
            reponse=reponse
        )
        return JsonResponse({'reply': reponse})

    except Exception as e:
        return JsonResponse({'reply': "Désolé, une erreur s'est produite. Réessaie."})


@login_required
def historique_view(request):
    historique= MessageChatbot.objects.filter(
        utilisateur=request.user
    ).order_by('-created_at')[:20]

    return JsonResponse({'history': [
        {
            'question': m.question,
            'reponse':  m.reponse,
            'date':     str(m.created_at)
        }
        for m in historique
    ]})