from django.urls import path

from .views import LoginView, RefreshView, SendOtpView, UserCheckView, VerifyOtpView


urlpatterns = [
    path('check-user', UserCheckView.as_view(), name='auth-check-user'),
    path('send-otp', SendOtpView.as_view(), name='auth-send-otp'),
    path('verify-otp', VerifyOtpView.as_view(), name='auth-verify-otp'),
    path('login', LoginView.as_view(), name='auth-login'),
    path('refresh', RefreshView.as_view(), name='auth-refresh'),
]
