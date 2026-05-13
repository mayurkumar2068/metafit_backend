from rest_framework import serializers

from accounts.models import User
from onboarding.models import OnboardingProfile


class ProfileSerializer(serializers.ModelSerializer):
    onboarding_complete = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'mobile_number',
            'email',
            'full_name',
            'onboarding_complete',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'mobile_number', 'is_active', 'created_at', 'updated_at']

    def get_onboarding_complete(self, obj):
        return OnboardingProfile.objects.filter(user=obj).exists()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email']
