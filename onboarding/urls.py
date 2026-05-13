from django.urls import path

from .views import CreateOnboardingProfileView, GetOnboardingProfileView

urlpatterns = [
    path('profile', CreateOnboardingProfileView.as_view(), name='onboarding-create'),
    path('profile/me', GetOnboardingProfileView.as_view(), name='onboarding-detail'),
]
