from django.db import models
from django.conf import settings


class OnboardingProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance'),
        ('general_health', 'General Health'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('active', 'Active'),
        ('very_active', 'Very Active'),
    ]

    DIETARY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_vegetarian', 'Non Vegetarian'),
        ('eggetarian', 'Eggetarian'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='onboarding_profile',
    )
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=30, choices=ACTIVITY_LEVEL_CHOICES)
    medical_conditions = models.JSONField(default=list, blank=True)
    dietary_preference = models.CharField(
        max_length=30,
        choices=DIETARY_CHOICES,
        blank=True,
        default='',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Onboarding Profile'
        verbose_name_plural = 'Onboarding Profiles'

    def __str__(self):
        return f'{self.user.full_name} - {self.goal}'
