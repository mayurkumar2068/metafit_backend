from django.contrib import admin

from .models import ExportJob


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'format', 'status', 'created_at')
    list_filter = ('status', 'format')
    search_fields = ('user__mobile_number', 'user__full_name')
