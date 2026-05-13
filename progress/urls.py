from django.urls import path

from .views import ProgressChartView, ProgressSummaryView

urlpatterns = [
    path('summary', ProgressSummaryView.as_view(), name='progress-summary'),
    path('chart', ProgressChartView.as_view(), name='progress-chart'),
]
