import os
import requests
import datetime
from events.models import Evenement
from groups.models import Groupe

def get_chatbot_response(message, user):
    api_key = os.environ.get('GROQ_API_KEY', '')

    # Récupérer les données réelles de l'utilisateur
    today = datetime.date.today()
    evenements = Evenement.objects.filter(
        createur=user, 
        date__gte=today
    ).order_by('date', 'heure_debut')[:10]
    groupes = user.groupes_rejoints.all()

    # Construire le contexte
    evt_text = "\n".join([
        f"- {e.titre} le {e.date} de {e.heure_debut} à {e.heure_fin} ({e.priorite})"
        for e in evenements
    ]) or "Aucun événement à venir."

    grp_text = ", ".join([g.nom for g in groupes]) or "Aucun groupe."

    system_prompt = f"""
Tu es un assistant de planning personnel pour un étudiant.
Réponds toujours en français, de façon courte et utile (2-3 phrases max).
N'invente pas d'informations.

Données de l'utilisateur ({user.username}) :
Événements à venir :
{evt_text}
Groupes : {grp_text}
Date du jour : {today}
"""

    if not api_key:
        return reponse_fallback(message, user, evenements)

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 200,
            "temperature": 0.5,
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return reponse_fallback(message, user, evenements)

    except Exception:
        return reponse_fallback(message, user, evenements)


def reponse_fallback(message, user, evenements):
    """Réponse sans API si Groq n'est pas disponible."""
    msg = message.lower()
    today = datetime.date.today()

    if any(m in msg for m in ["aujourd'hui", "ce soir"]):
        evts_today = [e for e in evenements if e.date == today]
        if evts_today:
            return f"Tu as {len(evts_today)} événement(s) aujourd'hui : " + ", ".join(e.titre for e in evts_today)
        return "Tu n'as aucun événement prévu aujourd'hui 👍"

    if "libre" in msg:
        if not evenements:
            return "Tu n'as aucun événement à venir — tu es totalement libre !"
        prochain = evenements[0]
        return f"Ton prochain événement est '{prochain.titre}' le {prochain.date} à {prochain.heure_debut}."

    if "groupe" in msg:
        groupes = user.groupes_rejoints.all()
        if groupes:
            return f"Tu es dans ces groupes : " + ", ".join(g.nom for g in groupes)
        return "Tu n'es dans aucun groupe pour le moment."

    if any(m in msg for m in ['bonjour', 'salut', 'hello']):
        return f"Bonjour {user.username} ! Comment puis-je t'aider avec ton emploi du temps ?"

    return "Je suis là pour t'aider avec ton emploi du temps ! Pose moi une question."