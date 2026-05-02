from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Book

BASE = '/api/books/'


def make_book(**kwargs):
    defaults = dict(
        title='El Quijote',
        author='Cervantes',
        published_year=1605,
        stock=5,
    )
    defaults.update(kwargs)
    return Book.objects.create(**defaults)


class BookListCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_empty(self):
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_list_returns_all_books(self):
        make_book()
        make_book(title='Cien años de soledad', author='García Márquez')
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_valid(self):
        payload = {'title': 'Rayuela', 'author': 'Cortázar', 'stock': 3}
        res = self.client.post(BASE, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'Rayuela')
        self.assertTrue(Book.objects.filter(title='Rayuela').exists())

    def test_create_missing_required_field(self):
        res = self.client.post(BASE, {'author': 'Sin título'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class BookDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = make_book()

    def test_retrieve_existing(self):
        res = self.client.get(f'{BASE}{self.book.pk}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.book.title)

    def test_retrieve_not_found(self):
        res = self.client.get(f'{BASE}99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing(self):
        payload = {'title': 'El Quijote II', 'author': 'Cervantes', 'stock': 10}
        res = self.client.put(f'{BASE}{self.book.pk}/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['stock'], 10)

    def test_update_not_found(self):
        res = self.client.put(f'{BASE}99999/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing(self):
        res = self.client.delete(f'{BASE}{self.book.pk}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_delete_not_found(self):
        res = self.client.delete(f'{BASE}99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
