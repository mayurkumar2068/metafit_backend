from django.urls import path

from .views import ProtocolCompleteDayView, ProtocolDetailView, ProtocolListCreateView

urlpatterns = [
    path('', ProtocolListCreateView.as_view(), name='protocol-list-create'),
    path('<int:pk>', ProtocolDetailView.as_view(), name='protocol-detail'),
    path('<int:pk>/complete-day', ProtocolCompleteDayView.as_view(), name='protocol-complete-day'),
]
