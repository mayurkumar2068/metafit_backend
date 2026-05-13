from rest_framework import serializers

from .models import ExportJob


class ExportJobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportJob
        fields = ['format', 'modules', 'from_date', 'to_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'processing'
        return super().create(validated_data)


class ExportJobReadSerializer(serializers.ModelSerializer):
    export_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = ExportJob
        fields = [
            'export_id',
            'format',
            'modules',
            'from_date',
            'to_date',
            'status',
            'download_url',
            'expires_at',
            'created_at',
        ]
