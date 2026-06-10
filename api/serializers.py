from rest_framework import serializers
from events.models import Evenement
from groups.models import Groupe
from notifications.models import Notification
class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'code_acces', 'membres']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'