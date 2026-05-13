from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import ExportJob
from .serializers import ExportJobCreateSerializer, ExportJobReadSerializer


class ExportCreateView(APIView):

    @swagger_auto_schema(
        operation_summary='Request data export',
        operation_description='Create an export job (PDF/CSV). Status starts as "processing".',
        request_body=ExportJobCreateSerializer,
        responses={202: ExportJobReadSerializer()},
        tags=['Exports'],
    )
    def post(self, request):
        serializer = ExportJobCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        return Response(
            ExportJobReadSerializer(job).data,
            status=status.HTTP_202_ACCEPTED,
        )


class ExportStatusView(APIView):

    @swagger_auto_schema(
        operation_summary='Get export status',
        operation_description='Check export job status and get download URL when ready.',
        responses={200: ExportJobReadSerializer()},
        tags=['Exports'],
    )
    def get(self, request, export_id):
        try:
            job = ExportJob.objects.get(id=export_id, user=request.user)
        except ExportJob.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ExportJobReadSerializer(job).data)
