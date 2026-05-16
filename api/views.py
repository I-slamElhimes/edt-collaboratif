from rest_framework import viewsets, permissions
from events.models import Evenement
from groups.models import Groupe
from notifications.models import Notification
from .serializers import EvenementSerializer, GroupeSerializer, NotificationSerializer

class EvenementViewSet(viewsets.ModelViewSet):
    serializer_class = EvenementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Evenement.objects.filter(createur=self.request.user)

class GroupeViewSet(viewsets.ModelViewSet):
    serializer_class = GroupeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Groupe.objects.filter(membres=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)