from django.contrib import admin

from .models import SideEffect


@admin.register(SideEffect)
class SideEffectAdmin(admin.ModelAdmin):
    list_display = ('user', 'symptom', 'severity', 'date', 'protocol')
    list_filter = ('severity', 'date')
    search_fields = ('symptom', 'user__mobile_number', 'user__full_name')
