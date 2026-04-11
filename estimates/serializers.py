from rest_framework import serializers
from .models import Estimate

class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['id', 'title', 'file', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']  # Эти поля нельзя менять через API
