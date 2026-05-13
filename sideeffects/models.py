from django.db import models
from django.conf import settings


class SideEffect(models.Model):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='side_effects',
    )
    protocol = models.ForeignKey(
        'protocols.Protocol',
        on_delete=models.CASCADE,
        related_name='side_effects',
        null=True,
        blank=True,
    )
    date = models.DateField()
    symptom = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.symptom} ({self.severity}) - {self.date}'
