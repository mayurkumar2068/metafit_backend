from django.urls import path

from .views import CheckinDetailView, CheckinListCreateView

urlpatterns = [
    path('', CheckinListCreateView.as_view(), name='checkin-list-create'),
    path('<int:pk>', CheckinDetailView.as_view(), name='checkin-detail'),
]
