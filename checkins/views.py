from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import DailyCheckin
from .serializers import DailyCheckinSerializer


class CheckinListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary='List check-ins',
        operation_description='List user check-ins (newest first). Optional date filters.',
        manual_parameters=[
            openapi.Parameter('from_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('to_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: DailyCheckinSerializer(many=True)},
        tags=['Check-ins'],
    )
    def get(self, request):
        qs = DailyCheckin.objects.filter(user=request.user)

        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        if from_date:
            qs = qs.filter(date__gte=from_date)
        if to_date:
            qs = qs.filter(date__lte=to_date)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        total = qs.count()
        results = DailyCheckinSerializer(qs[start:end], many=True).data

        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': results,
        })

    @swagger_auto_schema(
        operation_summary='Create check-in',
        operation_description='Submit daily check-in. One per date per user.',
        request_body=DailyCheckinSerializer,
        responses={201: DailyCheckinSerializer()},
        tags=['Check-ins'],
    )
    def post(self, request):
        serializer = DailyCheckinSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckinDetailView(APIView):

    def _get_checkin(self, request, pk):
        try:
            return DailyCheckin.objects.get(pk=pk, user=request.user)
        except DailyCheckin.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary='Get check-in detail',
        responses={200: DailyCheckinSerializer()},
        tags=['Check-ins'],
    )
    def get(self, request, pk):
        checkin = self._get_checkin(request, pk)
        if not checkin:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(DailyCheckinSerializer(checkin).data)

    @swagger_auto_schema(
        operation_summary='Update check-in',
        request_body=DailyCheckinSerializer,
        responses={200: DailyCheckinSerializer()},
        tags=['Check-ins'],
    )
    def patch(self, request, pk):
        checkin = self._get_checkin(request, pk)
        if not checkin:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DailyCheckinSerializer(
            checkin, data=request.data, partial=True, context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
