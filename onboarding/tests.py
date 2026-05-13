from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from .models import OnboardingProfile


class OnboardingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            mobile_number='9876543210',
            full_name='Mayur Bobade',
            email='mayur@example.com',
        )
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'age': 28,
            'gender': 'male',
            'height_cm': 175.0,
            'weight_kg': 72.5,
            'goal': 'weight_loss',
            'activity_level': 'moderate',
            'medical_conditions': ['diabetes', 'thyroid'],
            'dietary_preference': 'vegetarian',
        }

    def test_create_onboarding_profile(self):
        response = self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['onboarding_complete'])
        self.assertEqual(response.data['age'], 28)
        self.assertEqual(response.data['gender'], 'male')
        self.assertEqual(response.data['goal'], 'weight_loss')
        self.assertTrue(OnboardingProfile.objects.filter(user=self.user).exists())

    def test_duplicate_onboarding_rejected(self):
        self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        response = self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_onboarding_profile(self):
        self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        response = self.client.get(reverse('onboarding-detail'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['onboarding_complete'])
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['full_name'], 'Mayur Bobade')
        self.assertEqual(response.data['user']['mobile_number'], '9876543210')
        self.assertEqual(response.data['goal'], 'weight_loss')
        self.assertEqual(response.data['medical_conditions'], ['diabetes', 'thyroid'])

    def test_get_profile_404_when_not_completed(self):
        response = self.client.get(reverse('onboarding-detail'))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Onboarding not completed')

    def test_patch_onboarding_profile(self):
        self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        response = self.client.patch(
            reverse('onboarding-detail'),
            {'weight_kg': 70.0, 'goal': 'muscle_gain'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['weight_kg']), 70.0)
        self.assertEqual(response.data['goal'], 'muscle_gain')

    def test_unauthenticated_request_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            reverse('onboarding-create'),
            self.valid_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
