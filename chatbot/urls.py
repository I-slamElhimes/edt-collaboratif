from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('',        views.chatbot_page,    name='chat'),
    path('history/', views.historique_view, name='historique'),
]