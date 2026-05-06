from django.db import models
from django.contrib.auth.models import User

class MessageChatbot(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_chatbot')
    question    = models.TextField()
    reponse     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} : {self.question[:50]}"

    class Meta:
        ordering     = ['-created_at']
        verbose_name = "Message Chatbot"