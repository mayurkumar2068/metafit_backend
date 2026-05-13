from rest_framework import serializers

from .models import OnboardingProfile


class OnboardingProfileSerializer(serializers.ModelSerializer):
    """Used for creating/updating onboarding profile."""

    class Meta:
        model = OnboardingProfile
        fields = [
            'age',
            'gender',
            'height_cm',
            'weight_kg',
            'goal',
            'activity_level',
            'medical_conditions',
            'dietary_preference',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        if OnboardingProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {'detail': 'Onboarding profile already exists. Use PATCH to update.'}
            )
        return OnboardingProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    mobile_number = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)


class OnboardingProfileReadSerializer(serializers.ModelSerializer):
    """Used for reading onboarding profile in responses."""

    user = UserMiniSerializer(read_only=True)
    onboarding_complete = serializers.SerializerMethodField()

    class Meta:
        model = OnboardingProfile
        fields = [
            'id',
            'user',
            'onboarding_complete',
            'age',
            'gender',
            'height_cm',
            'weight_kg',
            'goal',
            'activity_level',
            'medical_conditions',
            'dietary_preference',
            'created_at',
            'updated_at',
        ]

    def get_onboarding_complete(self, obj):
        return True
