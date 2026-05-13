from django.db import models
from django.conf import settings


class DailyCheckin(models.Model):
    MOOD_CHOICES = [
        ('great', 'Great'),
        ('good', 'Good'),
        ('okay', 'Okay'),
        ('bad', 'Bad'),
        ('terrible', 'Terrible'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='checkins',
    )
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    energy_level = models.PositiveSmallIntegerField(help_text='1-10 scale')
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    water_litres = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    steps = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.full_name} - {self.date}'
