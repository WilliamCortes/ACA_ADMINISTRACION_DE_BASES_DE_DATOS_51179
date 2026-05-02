from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import User

BASE = '/api/users/'


def make_user(**kwargs):
    defaults = dict(
        user_name='Ana García',
        user_document='123456789',
        user_address='Calle 1 # 2-3',
        user_email='ana@example.com',
        user_phone_number='3001234567',
    )
    defaults.update(kwargs)
    return User.objects.create(**defaults)


class UserListCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_empty(self):
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_list_returns_all_users(self):
        make_user()
        make_user(user_name='Pedro', user_document='999', user_email='pedro@example.com')
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_valid(self):
        payload = {
            'user_name': 'Luis López',
            'user_document': '55566677',
            'user_address': 'Av. Siempre Viva',
            'user_email': 'luis@example.com',
            'user_phone_number': '3109876543',
        }
        res = self.client.post(BASE, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user_name'], payload['user_name'])
        self.assertTrue(User.objects.filter(user_document='55566677').exists())

    def test_create_missing_required_field(self):
        res = self.client.post(BASE, {'user_name': 'Sin email'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()

    def test_retrieve_existing(self):
        res = self.client.get(f'{BASE}{self.user.pk}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user_document'], self.user.user_document)

    def test_retrieve_not_found(self):
        res = self.client.get(f'{BASE}99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing(self):
        payload = {
            'user_name': 'Ana Actualizada',
            'user_document': self.user.user_document,
            'user_address': self.user.user_address,
            'user_email': self.user.user_email,
            'user_phone_number': self.user.user_phone_number,
        }
        res = self.client.put(f'{BASE}{self.user.pk}/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user_name'], 'Ana Actualizada')

    def test_update_not_found(self):
        res = self.client.put(f'{BASE}99999/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing(self):
        res = self.client.delete(f'{BASE}{self.user.pk}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_not_found(self):
        res = self.client.delete(f'{BASE}99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
