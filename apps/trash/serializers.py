from rest_framework import serializers
from .models import Trash

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = '__all__'
