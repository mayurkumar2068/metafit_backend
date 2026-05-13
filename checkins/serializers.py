from rest_framework import serializers

from .models import DailyCheckin


class DailyCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckin
        fields = [
            'id',
            'date',
            'weight_kg',
            'mood',
            'energy_level',
            'sleep_hours',
            'water_litres',
            'steps',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        date = data.get('date')
        if self.instance is None and DailyCheckin.objects.filter(user=user, date=date).exists():
            raise serializers.ValidationError({'date': 'Check-in already exists for this date.'})
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
