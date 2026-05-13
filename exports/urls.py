from django.urls import path

from .views import ExportCreateView, ExportStatusView

urlpatterns = [
    path('', ExportCreateView.as_view(), name='export-create'),
    path('<uuid:export_id>', ExportStatusView.as_view(), name='export-status'),
]
