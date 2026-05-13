from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
import secrets

from .models import User

OTP_TTL_SECONDS = 300


class SendOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)

    def validate_mobile_number(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('mobile_number is required')
        return cleaned

    def send_otp(self):
        mobile_number = self.validated_data['mobile_number']
        otp = f'{secrets.randbelow(900000) + 100000}'
        cache.set(f'otp:{mobile_number}', otp, timeout=OTP_TTL_SECONDS)
        return {
            'mobile_number': mobile_number,
            'otp_required': True,
            'otp_sent': True,
            'expires_in_seconds': OTP_TTL_SECONDS,
            # Dev-only response field; remove in production SMS integration.
            'debug_otp': otp,
        }


class VerifyOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6)
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_mobile_number(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('mobile_number is required')
        return cleaned

    def validate_full_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('full_name is required')
        return cleaned

    def validate_otp(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('otp is required')
        if len(cleaned) != 6 or not cleaned.isdigit():
            raise serializers.ValidationError('otp must be a 6-digit number')
        return cleaned

    def verify_and_authenticate(self):
        mobile_number = self.validated_data['mobile_number']
        otp = self.validated_data['otp']
        full_name = self.validated_data['full_name']
        email = self.validated_data.get('email') or None

        cached_otp = cache.get(f'otp:{mobile_number}')
        if not cached_otp:
            raise serializers.ValidationError({'otp': 'OTP expired or not requested'})
        if cached_otp != otp:
            raise serializers.ValidationError({'otp': 'Invalid OTP'})

        cache.delete(f'otp:{mobile_number}')

        user, created = User.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={
                'full_name': full_name,
                'email': email,
            },
        )
        if not created:
            changed = False
            if user.full_name != full_name:
                user.full_name = full_name
                changed = True
            if email and user.email != email:
                user.email = email
                changed = True
            if changed:
                user.save(update_fields=['full_name', 'email', 'updated_at'])

        refresh = RefreshToken.for_user(user)
        return {
            'is_new_user': created,
            'auth_mode': 'register' if created else 'login',
            'otp_required': True,
            'otp_verified': True,
            'user': {
                'id': user.id,
                'mobile_number': user.mobile_number,
                'email': user.email,
                'full_name': user.full_name,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        }


class UserCheckSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)

    def validate_mobile_number(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('mobile_number is required')
        return cleaned

    def build_check_response(self):
        mobile_number = self.validated_data['mobile_number']
        exists = User.objects.filter(mobile_number=mobile_number).exists()
        return {
            'mobile_number': mobile_number,
            'is_new_user': not exists,
            'auth_mode': 'register' if not exists else 'login',
            'otp_required': True,
        }


class MobileLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_mobile_number(self, value):
        return value.strip()

    def validate_full_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError('full_name is required')
        return cleaned

    def create_or_update_user(self):
        mobile_number = self.validated_data['mobile_number']
        full_name = self.validated_data['full_name']
        email = self.validated_data.get('email') or None

        user, created = User.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={
                'full_name': full_name,
                'email': email,
            },
        )
        if not created:
            changed = False
            if user.full_name != full_name:
                user.full_name = full_name
                changed = True
            if email and user.email != email:
                user.email = email
                changed = True
            if changed:
                user.save(update_fields=['full_name', 'email', 'updated_at'])
        return user, created

    @staticmethod
    def build_auth_response(user, is_new_user=False):
        refresh = RefreshToken.for_user(user)
        return {
            'is_new_user': is_new_user,
            'auth_mode': 'register' if is_new_user else 'login',
            'otp_required': True,
            'user': {
                'id': user.id,
                'mobile_number': user.mobile_number,
                'email': user.email,
                'full_name': user.full_name,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        }
