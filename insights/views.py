from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Insight
from .serializers import InsightSerializer


class InsightListView(APIView):

    @swagger_auto_schema(
        operation_summary='List insights',
        operation_description='List AI/rule-based insights for the logged-in user.',
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              enum=['weight', 'sleep', 'energy', 'water', 'mood', 'general']),
        ],
        responses={200: InsightSerializer(many=True)},
        tags=['Insights'],
    )
    def get(self, request):
        qs = Insight.objects.filter(user=request.user)

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        total = qs.count()
        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': InsightSerializer(qs[start:end], many=True).data,
        })
