from rest_framework import serializers

from .models import Insight


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ['id', 'title', 'body', 'category', 'severity', 'created_at']
        read_only_fields = ['id', 'created_at']
