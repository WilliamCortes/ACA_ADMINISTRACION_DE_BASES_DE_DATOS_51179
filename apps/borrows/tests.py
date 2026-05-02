from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import User
from apps.books.models import Book
from .models import Borrow
from .services import BorrowService

BASE = '/api/borrows/'
DUE = (date.today() + timedelta(days=14)).isoformat()


def make_user():
    return User.objects.create(
        user_name='Test User', user_document='111',
        user_address='Calle 0', user_email='test@example.com',
        user_phone_number='300000000',
    )


def make_book(stock=3):
    return Book.objects.create(title='Test Book', author='Author', stock=stock)


def make_borrow(user, book, status_val='BORROWED'):
    b = Borrow.objects.create(user=user, book=book, due_date=DUE)
    if status_val != 'BORROWED':
        b.status = status_val
        b.save()
    return b


# ── API tests ────────────────────────────────────────────────────────────────

class BorrowListRetrieveTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.book = make_book()

    def test_list_empty(self):
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_list_returns_borrows(self):
        make_borrow(self.user, self.book)
        res = self.client.get(BASE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_retrieve_existing(self):
        borrow = make_borrow(self.user, self.book)
        res = self.client.get(f'{BASE}{borrow.pk}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_not_found(self):
        res = self.client.get(f'{BASE}99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CreateBorrowAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.book = make_book(stock=2)

    def test_create_borrow_success(self):
        payload = {'user': self.user.pk, 'book': self.book.pk, 'due_date': DUE}
        res = self.client.post(f'{BASE}create_borrow/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 1)

    def test_create_borrow_no_stock(self):
        self.book.stock = 0
        self.book.save()
        payload = {'user': self.user.pk, 'book': self.book.pk, 'due_date': DUE}
        res = self.client.post(f'{BASE}create_borrow/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_borrow_missing_fields(self):
        res = self.client.post(f'{BASE}create_borrow/', {'user': self.user.pk}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_borrow_book_not_found(self):
        payload = {'user': self.user.pk, 'book': 99999, 'due_date': DUE}
        res = self.client.post(f'{BASE}create_borrow/', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ReturnBookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.book = make_book()

    def test_return_book_success(self):
        borrow = make_borrow(self.user, self.book)
        res = self.client.patch(f'{BASE}{borrow.pk}/return_book/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'RETURNED')
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 4)

    def test_return_book_already_returned(self):
        borrow = make_borrow(self.user, self.book, status_val='RETURNED')
        res = self.client.patch(f'{BASE}{borrow.pk}/return_book/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_book_not_found(self):
        res = self.client.patch(f'{BASE}99999/return_book/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


# ── Service unit tests ────────────────────────────────────────────────────────

class BorrowServiceTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book(stock=2)

    def test_create_borrow_decrements_stock(self):
        BorrowService.create_borrow(self.user.pk, self.book.pk, DUE)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 1)

    def test_create_borrow_no_stock_raises(self):
        self.book.stock = 0
        self.book.save()
        with self.assertRaises(ValueError):
            BorrowService.create_borrow(self.user.pk, self.book.pk, DUE)

    def test_create_borrow_invalid_book_raises(self):
        with self.assertRaises(ValueError):
            BorrowService.create_borrow(self.user.pk, 99999, DUE)

    def test_return_book_sets_status_and_date(self):
        borrow = make_borrow(self.user, self.book)
        result = BorrowService.return_book(borrow.pk)
        self.assertEqual(result.status, 'RETURNED')
        self.assertEqual(result.return_date, date.today())

    def test_return_book_increments_stock(self):
        borrow = make_borrow(self.user, self.book)
        BorrowService.return_book(borrow.pk)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 3)

    def test_return_book_already_returned_raises(self):
        borrow = make_borrow(self.user, self.book, status_val='RETURNED')
        with self.assertRaises(ValueError):
            BorrowService.return_book(borrow.pk)

    def test_check_overdue_marks_late(self):
        yesterday = date.today() - timedelta(days=1)
        borrow = Borrow.objects.create(user=self.user, book=self.book, due_date=yesterday)
        updated = BorrowService.check_overdue()
        self.assertEqual(updated, 1)
        borrow.refresh_from_db()
        self.assertEqual(borrow.status, 'LATE')
