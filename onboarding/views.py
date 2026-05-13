from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import OnboardingProfile
from .serializers import OnboardingProfileReadSerializer, OnboardingProfileSerializer


class CreateOnboardingProfileView(APIView):

    @swagger_auto_schema(
        operation_summary='Create onboarding profile',
        operation_description='Save onboarding data after first registration. One profile per user.',
        request_body=OnboardingProfileSerializer,
        responses={
            201: openapi.Response(
                description='Profile created',
                examples={
                    'application/json': {
                        'id': 1,
                        'user_id': 1,
                        'onboarding_complete': True,
                        'age': 28,
                        'gender': 'male',
                        'height_cm': 175.0,
                        'weight_kg': 72.5,
                        'goal': 'weight_loss',
                        'activity_level': 'moderate',
                        'medical_conditions': ['diabetes', 'thyroid'],
                        'dietary_preference': 'vegetarian',
                        'created_at': '2026-05-12T06:00:00Z',
                        'updated_at': '2026-05-12T06:00:00Z',
                    }
                },
            ),
            400: 'Validation error / Profile already exists',
        },
        tags=['Onboarding'],
    )
    def post(self, request):
        serializer = OnboardingProfileSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        read_serializer = OnboardingProfileReadSerializer(profile)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class GetOnboardingProfileView(APIView):

    @swagger_auto_schema(
        operation_summary='Get onboarding profile',
        operation_description='Fetch the logged-in user\'s onboarding profile.',
        responses={
            200: openapi.Response(
                description='Profile found',
                examples={
                    'application/json': {
                        'id': 1,
                        'user_id': 1,
                        'onboarding_complete': True,
                        'age': 28,
                        'gender': 'male',
                        'height_cm': 175.0,
                        'weight_kg': 72.5,
                        'goal': 'weight_loss',
                        'activity_level': 'moderate',
                        'medical_conditions': ['diabetes', 'thyroid'],
                        'dietary_preference': 'vegetarian',
                        'created_at': '2026-05-12T06:00:00Z',
                        'updated_at': '2026-05-12T06:00:00Z',
                    }
                },
            ),
            404: 'Onboarding not completed',
        },
        tags=['Onboarding'],
    )
    def get(self, request):
        try:
            profile = OnboardingProfile.objects.get(user=request.user)
        except OnboardingProfile.DoesNotExist:
            return Response(
                {'detail': 'Onboarding not completed'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OnboardingProfileReadSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update onboarding profile',
        operation_description='Partially update the logged-in user\'s onboarding profile.',
        request_body=OnboardingProfileSerializer,
        responses={
            200: 'Updated profile',
            404: 'Onboarding not completed',
        },
        tags=['Onboarding'],
    )
    def patch(self, request):
        try:
            profile = OnboardingProfile.objects.get(user=request.user)
        except OnboardingProfile.DoesNotExist:
            return Response(
                {'detail': 'Onboarding not completed'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OnboardingProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        read_serializer = OnboardingProfileReadSerializer(profile)
        return Response(read_serializer.data, status=status.HTTP_200_OK)
