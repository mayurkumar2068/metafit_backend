from django.contrib import admin

from .models import Protocol, ProtocolDayLog


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'start_date', 'end_date', 'total_days')
    list_filter = ('status',)
    search_fields = ('name', 'user__mobile_number', 'user__full_name')


@admin.register(ProtocolDayLog)
class ProtocolDayLogAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'date', 'completed_tasks')
    list_filter = ('date',)
