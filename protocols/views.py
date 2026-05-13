from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import Protocol, ProtocolDayLog
from .serializers import CompleteDaySerializer, ProtocolDayLogSerializer, ProtocolSerializer


class ProtocolListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary='List protocols',
        operation_description='List all protocols for the logged-in user.',
        responses={200: ProtocolSerializer(many=True)},
        tags=['Protocols'],
    )
    def get(self, request):
        qs = Protocol.objects.filter(user=request.user)
        return Response({'results': ProtocolSerializer(qs, many=True).data})

    @swagger_auto_schema(
        operation_summary='Create protocol',
        request_body=ProtocolSerializer,
        responses={201: ProtocolSerializer()},
        tags=['Protocols'],
    )
    def post(self, request):
        serializer = ProtocolSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProtocolDetailView(APIView):

    def _get_protocol(self, request, pk):
        try:
            return Protocol.objects.get(pk=pk, user=request.user)
        except Protocol.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary='Get protocol detail',
        responses={200: ProtocolSerializer()},
        tags=['Protocols'],
    )
    def get(self, request, pk):
        protocol = self._get_protocol(request, pk)
        if not protocol:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = ProtocolSerializer(protocol).data
        data['day_logs'] = ProtocolDayLogSerializer(
            protocol.day_logs.all(), many=True
        ).data
        return Response(data)


class ProtocolCompleteDayView(APIView):

    @swagger_auto_schema(
        operation_summary='Complete protocol day',
        operation_description='Mark tasks as completed for a given date.',
        request_body=CompleteDaySerializer,
        responses={200: ProtocolDayLogSerializer()},
        tags=['Protocols'],
    )
    def post(self, request, pk):
        try:
            protocol = Protocol.objects.get(pk=pk, user=request.user)
        except Protocol.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompleteDaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        log, created = ProtocolDayLog.objects.update_or_create(
            protocol=protocol,
            date=serializer.validated_data['date'],
            defaults={'completed_tasks': serializer.validated_data['completed_tasks']},
        )
        return Response(ProtocolDayLogSerializer(log).data)
