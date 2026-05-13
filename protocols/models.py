from django.db import models
from django.conf import settings


class Protocol(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='protocols',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField()
    tasks_per_day = models.JSONField(
        default=list,
        blank=True,
        help_text='List of task keys e.g. ["morning_walk","supplements","diet_followed"]',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.name} ({self.user.full_name})'

    @property
    def day_number(self):
        from django.utils import timezone
        today = timezone.now().date()
        if today < self.start_date:
            return 0
        delta = (today - self.start_date).days + 1
        return min(delta, self.total_days)


class ProtocolDayLog(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='day_logs')
    date = models.DateField()
    completed_tasks = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('protocol', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.protocol.name} - {self.date}'
