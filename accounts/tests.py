from django.urls import reverse
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AuthApiTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_check_user_returns_register_mode_for_new_user(self):
        payload = {
            'mobile_number': '9999999999',
        }

        response = self.client.post(reverse('auth-check-user'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_new_user'])
        self.assertEqual(response.data['auth_mode'], 'register')
        self.assertTrue(response.data['otp_required'])

    def test_check_user_returns_login_mode_for_existing_user(self):
        User.objects.create_user(
            mobile_number='9876543210',
            full_name='Mayur Bobade',
            email='mayur@example.com',
        )
        payload = {
            'mobile_number': '9876543210',
        }

        response = self.client.post(reverse('auth-check-user'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_new_user'])
        self.assertEqual(response.data['auth_mode'], 'login')
        self.assertTrue(response.data['otp_required'])

    def test_send_otp_returns_success_payload(self):
        payload = {'mobile_number': '9999999999'}

        response = self.client.post(reverse('auth-send-otp'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mobile_number'], '9999999999')
        self.assertTrue(response.data['otp_sent'])
        self.assertTrue(response.data['otp_required'])
        self.assertIn('debug_otp', response.data)

    def test_verify_otp_authenticates_new_user(self):
        send_payload = {'mobile_number': '9999999999'}
        send_response = self.client.post(reverse('auth-send-otp'), send_payload, format='json')
        otp = send_response.data['debug_otp']

        verify_payload = {
            'mobile_number': '9999999999',
            'otp': otp,
            'full_name': 'Mayur Bobade',
            'email': 'mayur@example.com',
        }
        response = self.client.post(reverse('auth-verify-otp'), verify_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['otp_verified'])
        self.assertTrue(response.data['is_new_user'])
        self.assertEqual(response.data['auth_mode'], 'register')
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_verify_otp_fails_for_invalid_code(self):
        send_payload = {'mobile_number': '9999999999'}
        self.client.post(reverse('auth-send-otp'), send_payload, format='json')

        verify_payload = {
            'mobile_number': '9999999999',
            'otp': '000000',
            'full_name': 'Mayur Bobade',
            'email': 'mayur@example.com',
        }
        response = self.client.post(reverse('auth-verify-otp'), verify_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('otp', response.data)

    def test_login_creates_user_and_returns_tokens(self):
        payload = {
            'mobile_number': '9876543210',
            'full_name': 'Mayur Bobade',
            'email': 'mayur@example.com',
        }

        response = self.client.post(reverse('auth-login'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_new_user'])
        self.assertEqual(response.data['auth_mode'], 'register')
        self.assertTrue(response.data['otp_required'])
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertTrue(User.objects.filter(mobile_number='9876543210').exists())

    def test_login_existing_user_returns_login_mode_flag(self):
        User.objects.create_user(
            mobile_number='9876543210',
            full_name='Mayur Bobade',
            email='mayur@example.com',
        )
        payload = {
            'mobile_number': '9876543210',
            'full_name': 'Mayur Bobade',
            'email': 'mayur@example.com',
        }

        response = self.client.post(reverse('auth-login'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_new_user'])
        self.assertEqual(response.data['auth_mode'], 'login')
        self.assertTrue(response.data['otp_required'])
