import uuid
from django.db import models
from django.conf import settings


class ExportJob(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
    ]

    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_jobs',
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    modules = models.JSONField(default=list, help_text='e.g. ["checkins","progress","side_effects"]')
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    download_url = models.CharField(max_length=500, blank=True, default='')
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Export {self.id} ({self.status})'
