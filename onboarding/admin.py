from django.contrib import admin

from .models import OnboardingProfile


@admin.register(OnboardingProfile)
class OnboardingProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'goal', 'activity_level', 'created_at')
    list_filter = ('gender', 'goal', 'activity_level')
    search_fields = ('user__mobile_number', 'user__full_name')
    readonly_fields = ('created_at', 'updated_at')
