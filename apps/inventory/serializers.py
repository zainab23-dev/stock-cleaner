from rest_framework import serializers
from .models import DataRow

class DataRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRow
        fields = '__all__'
