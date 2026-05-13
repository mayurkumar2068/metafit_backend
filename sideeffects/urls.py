from django.urls import path

from .views import SideEffectDetailView, SideEffectListCreateView

urlpatterns = [
    path('', SideEffectListCreateView.as_view(), name='sideeffect-list-create'),
    path('<int:pk>', SideEffectDetailView.as_view(), name='sideeffect-detail'),
]
