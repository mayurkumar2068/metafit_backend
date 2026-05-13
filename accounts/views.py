from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    MobileLoginSerializer,
    SendOtpSerializer,
    UserCheckSerializer,
    VerifyOtpSerializer,
)


class UserCheckView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Check user by mobile number',
        operation_description='Returns whether the mobile number is a new user or existing user.',
        request_body=UserCheckSerializer,
        responses={
            200: openapi.Response(
                description='User existence checked',
                examples={
                    'application/json': {
                        'mobile_number': '9876543210',
                        'is_new_user': False,
                        'auth_mode': 'login',
                        'otp_required': True,
                    }
                },
            ),
            400: 'Validation error',
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = UserCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.build_check_response()
        return Response(payload, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Send OTP',
        operation_description='Generates OTP for given mobile number. In dev mode response includes debug_otp.',
        request_body=SendOtpSerializer,
        responses={
            200: openapi.Response(
                description='OTP sent successfully',
                examples={
                    'application/json': {
                        'mobile_number': '9876543210',
                        'otp_required': True,
                        'otp_sent': True,
                        'expires_in_seconds': 300,
                        'debug_otp': '123456',
                    }
                },
            ),
            400: 'Validation error',
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.send_otp()
        return Response(payload, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Verify OTP and authenticate user',
        operation_description='Verifies OTP, then registers new user or logs in existing user and returns JWT tokens.',
        request_body=VerifyOtpSerializer,
        responses={
            200: openapi.Response(
                description='OTP verified and user authenticated',
                examples={
                    'application/json': {
                        'is_new_user': True,
                        'auth_mode': 'register',
                        'otp_required': True,
                        'otp_verified': True,
                        'user': {
                            'id': 1,
                            'mobile_number': '9876543210',
                            'email': 'mayur@example.com',
                            'full_name': 'Mayur Bobade',
                        },
                        'tokens': {
                            'access': '<jwt-access-token>',
                            'refresh': '<jwt-refresh-token>',
                        },
                    }
                },
            ),
            400: 'Validation error / Invalid OTP',
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.verify_and_authenticate()
        return Response(payload, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Login/Create user (legacy)',
        operation_description='Creates user if not exists or updates existing user, then returns JWT tokens.',
        request_body=MobileLoginSerializer,
        responses={
            200: openapi.Response(
                description='User authenticated',
                examples={
                    'application/json': {
                        'is_new_user': False,
                        'auth_mode': 'login',
                        'otp_required': True,
                        'user': {
                            'id': 1,
                            'mobile_number': '9876543210',
                            'email': 'mayur@example.com',
                            'full_name': 'Mayur Bobade',
                        },
                        'tokens': {
                            'access': '<jwt-access-token>',
                            'refresh': '<jwt-refresh-token>',
                        },
                    }
                },
            ),
            400: 'Validation error',
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = MobileLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = serializer.create_or_update_user()
        payload = serializer.build_auth_response(user, is_new_user=created)
        return Response(payload, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
