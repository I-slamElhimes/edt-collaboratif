from django.contrib import admin
from .models import MessageChatbot

@admin.register(MessageChatbot)
class MessageChatbotAdmin(admin.ModelAdmin):
    list_display  = ['utilisateur', 'question', 'created_at']
    search_fields = ['utilisateur__username', 'question']