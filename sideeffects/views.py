from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import SideEffect
from .serializers import SideEffectSerializer


class SideEffectListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary='List side effects',
        operation_description='List user side effects. Optional protocol filter.',
        manual_parameters=[
            openapi.Parameter('protocol_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: SideEffectSerializer(many=True)},
        tags=['Side Effects'],
    )
    def get(self, request):
        qs = SideEffect.objects.filter(user=request.user)

        protocol_id = request.query_params.get('protocol_id')
        if protocol_id:
            qs = qs.filter(protocol_id=protocol_id)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        total = qs.count()
        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': SideEffectSerializer(qs[start:end], many=True).data,
        })

    @swagger_auto_schema(
        operation_summary='Log side effect',
        request_body=SideEffectSerializer,
        responses={201: SideEffectSerializer()},
        tags=['Side Effects'],
    )
    def post(self, request):
        serializer = SideEffectSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SideEffectDetailView(APIView):

    @swagger_auto_schema(
        operation_summary='Get side effect detail',
        responses={200: SideEffectSerializer()},
        tags=['Side Effects'],
    )
    def get(self, request, pk):
        try:
            se = SideEffect.objects.get(pk=pk, user=request.user)
        except SideEffect.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SideEffectSerializer(se).data)
