import os
import requests

def get_chatbot_response(message, user):
    api_key = os.environ.get('GROQ_API_KEY', '')

    if not api_key:
        return reponse_fallback(message)

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant pour une application de gestion "
                        "d'emploi du temps scolaire. Réponds toujours en français, "
                        "de façon courte et utile (2-3 phrases max)."
                    )
                },
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return reponse_fallback(message)

    except Exception:
        return reponse_fallback(message)


def reponse_fallback(message):
    msg = message.lower()
    if any(m in msg for m in ['bonjour', 'salut', 'hello']):
        return "Bonjour ! Je suis ton assistant EDT. Comment puis-je t'aider ?"
    elif any(m in msg for m in ['cours', 'examen', 'exam']):
        return "Tu peux ajouter tes cours dans la section Événements."
    elif any(m in msg for m in ['groupe', 'équipe']):
        return "Rejoins ou crée un groupe dans la section Groupes."
    else:
        return "Je suis là pour t'aider avec ton emploi du temps !"