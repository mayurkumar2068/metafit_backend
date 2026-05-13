from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from checkins.models import DailyCheckin


class ProgressSummaryView(APIView):

    @swagger_auto_schema(
        operation_summary='Progress summary',
        operation_description='Overall progress stats computed from check-in data.',
        responses={
            200: openapi.Response(
                description='Summary stats',
                examples={
                    'application/json': {
                        'total_checkins': 45,
                        'streak_days': 12,
                        'weight_start_kg': 75.0,
                        'weight_current_kg': 71.8,
                        'weight_change_kg': -3.2,
                        'avg_sleep_hours': 7.2,
                        'avg_energy_level': 6.8,
                        'avg_water_litres': 2.8,
                    }
                },
            ),
        },
        tags=['Progress'],
    )
    def get(self, request):
        qs = DailyCheckin.objects.filter(user=request.user)
        total = qs.count()

        agg = qs.aggregate(
            avg_sleep=Avg('sleep_hours'),
            avg_energy=Avg('energy_level'),
            avg_water=Avg('water_litres'),
        )

        weight_first = qs.filter(weight_kg__isnull=False).order_by('date').values_list('weight_kg', flat=True).first()
        weight_last = qs.filter(weight_kg__isnull=False).order_by('-date').values_list('weight_kg', flat=True).first()

        weight_start = float(weight_first) if weight_first else None
        weight_current = float(weight_last) if weight_last else None
        weight_change = round(weight_current - weight_start, 1) if (weight_start and weight_current) else None

        streak = 0
        today = timezone.now().date()
        day = today
        while qs.filter(date=day).exists():
            streak += 1
            day -= timedelta(days=1)

        return Response({
            'total_checkins': total,
            'streak_days': streak,
            'weight_start_kg': weight_start,
            'weight_current_kg': weight_current,
            'weight_change_kg': weight_change,
            'avg_sleep_hours': round(float(agg['avg_sleep']), 1) if agg['avg_sleep'] else None,
            'avg_energy_level': round(float(agg['avg_energy']), 1) if agg['avg_energy'] else None,
            'avg_water_litres': round(float(agg['avg_water']), 1) if agg['avg_water'] else None,
        })


class ProgressChartView(APIView):

    @swagger_auto_schema(
        operation_summary='Progress chart data',
        operation_description='Time-series data for charting. Metric: weight, sleep, energy, water, steps.',
        manual_parameters=[
            openapi.Parameter('metric', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              enum=['weight', 'sleep', 'energy', 'water', 'steps'], required=True),
            openapi.Parameter('period', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              enum=['7d', '30d', '90d'], default='30d'),
        ],
        tags=['Progress'],
    )
    def get(self, request):
        metric = request.query_params.get('metric', 'weight')
        period = request.query_params.get('period', '30d')

        days = {'7d': 7, '30d': 30, '90d': 90}.get(period, 30)
        since = timezone.now().date() - timedelta(days=days)

        metric_field_map = {
            'weight': 'weight_kg',
            'sleep': 'sleep_hours',
            'energy': 'energy_level',
            'water': 'water_litres',
            'steps': 'steps',
        }
        field = metric_field_map.get(metric)
        if not field:
            return Response({'detail': 'Invalid metric'}, status=400)

        qs = (
            DailyCheckin.objects
            .filter(user=request.user, date__gte=since)
            .exclude(**{f'{field}__isnull': True})
            .order_by('date')
            .values_list('date', field)
        )

        data = [{'date': str(d), 'value': float(v)} for d, v in qs]

        return Response({
            'metric': metric,
            'period': period,
            'data': data,
        })
