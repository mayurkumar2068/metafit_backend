from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProfileSerializer, ProfileUpdateSerializer


class ProfileView(APIView):

    @swagger_auto_schema(
        operation_summary='Get profile',
        operation_description='Get current authenticated user profile.',
        responses={200: ProfileSerializer()},
        tags=['Profile'],
    )
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    @swagger_auto_schema(
        operation_summary='Update profile',
        operation_description='Update full_name and/or email.',
        request_body=ProfileUpdateSerializer,
        responses={200: ProfileSerializer()},
        tags=['Profile'],
    )
    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProfileSerializer(request.user).data)

    @swagger_auto_schema(
        operation_summary='Delete account',
        operation_description='Soft-delete (deactivate) the user account.',
        responses={204: 'Account deactivated'},
        tags=['Profile'],
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)
