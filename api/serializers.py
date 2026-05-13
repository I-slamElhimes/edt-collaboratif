from rest_framework import serializers
from events.models import Evenement
from groups.models import Groupe

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'code_acces', 'membres']