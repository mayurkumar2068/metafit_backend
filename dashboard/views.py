from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from checkins.models import DailyCheckin
from checkins.serializers import DailyCheckinSerializer
from protocols.models import Protocol
from protocols.serializers import ProtocolSerializer
from insights.models import Insight
from insights.serializers import InsightSerializer


class HomeDashboardView(APIView):

    @swagger_auto_schema(
        operation_summary='Home dashboard',
        operation_description='Aggregated home screen data: today check-in, active protocol, streak, recent insights.',
        responses={
            200: openapi.Response(
                description='Dashboard data',
                examples={
                    'application/json': {
                        'user': {'full_name': 'Mayur Bobade', 'streak_days': 12},
                        'today_checkin': None,
                        'active_protocol': None,
                        'recent_insights': [],
                    }
                },
            ),
        },
        tags=['Dashboard'],
    )
    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Streak calculation
        streak = 0
        day = today
        while DailyCheckin.objects.filter(user=user, date=day).exists():
            streak += 1
            day -= timedelta(days=1)

        # Today's check-in
        today_checkin = DailyCheckin.objects.filter(user=user, date=today).first()
        today_data = DailyCheckinSerializer(today_checkin).data if today_checkin else None

        # Active protocol
        active_protocol = Protocol.objects.filter(user=user, status='active').first()
        protocol_data = ProtocolSerializer(active_protocol).data if active_protocol else None

        # Recent insights (last 5)
        recent_insights = Insight.objects.filter(user=user)[:5]
        insights_data = InsightSerializer(recent_insights, many=True).data

        return Response({
            'user': {
                'full_name': user.full_name,
                'streak_days': streak,
            },
            'today_checkin': today_data,
            'active_protocol': protocol_data,
            'recent_insights': insights_data,
        })
