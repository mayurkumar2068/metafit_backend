from django.contrib import admin

from .models import Insight


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'severity', 'created_at')
    list_filter = ('category', 'severity')
    search_fields = ('title', 'user__mobile_number', 'user__full_name')
