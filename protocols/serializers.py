from rest_framework import serializers

from .models import Protocol, ProtocolDayLog


class ProtocolSerializer(serializers.ModelSerializer):
    day_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Protocol
        fields = [
            'id',
            'name',
            'description',
            'status',
            'start_date',
            'end_date',
            'total_days',
            'tasks_per_day',
            'day_number',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'day_number', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProtocolDayLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolDayLog
        fields = ['id', 'protocol', 'date', 'completed_tasks', 'created_at']
        read_only_fields = ['id', 'created_at']


class CompleteDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    completed_tasks = serializers.ListField(child=serializers.CharField())
