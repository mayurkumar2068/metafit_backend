from django.db import models
from django.conf import settings


class Insight(models.Model):
    CATEGORY_CHOICES = [
        ('weight', 'Weight'),
        ('sleep', 'Sleep'),
        ('energy', 'Energy'),
        ('water', 'Water'),
        ('mood', 'Mood'),
        ('general', 'General'),
    ]

    SEVERITY_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('warning', 'Warning'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='insights',
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
