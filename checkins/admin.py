from django.contrib import admin

from .models import DailyCheckin


@admin.register(DailyCheckin)
class DailyCheckinAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood', 'energy_level', 'weight_kg', 'sleep_hours')
    list_filter = ('mood', 'date')
    search_fields = ('user__mobile_number', 'user__full_name')
