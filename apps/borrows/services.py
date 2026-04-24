from datetime import date

from apps.books.repositories import BookRepository
from apps.users.repositories import UserRepository
from .models import Borrow
from .repositories import BorrowRepository


class BorrowService:

    @staticmethod
    def create_borrow(user_id: int, book_id: int, due_date) -> Borrow:
        book = BookRepository.get_by_id(book_id)
        if book is None:
            raise ValueError(f"Libro con id={book_id} no existe.")

        if book.stock <= 0:
            raise ValueError("No hay stock disponible para este libro.")

        borrow = BorrowRepository.create(user_id, book_id, due_date)

        book.stock -= 1
        book.save()

        return borrow

    @staticmethod
    def return_book(borrow_id: int) -> Borrow:
        borrow = BorrowRepository.get_by_id(borrow_id)
        if borrow is None:
            raise ValueError(f"Préstamo con id={borrow_id} no existe.")

        if borrow.status == 'RETURNED':
            raise ValueError("Este préstamo ya fue devuelto.")

        borrow.status = 'RETURNED'
        borrow.return_date = date.today()
        BorrowRepository.save(borrow)

        borrow.book.stock += 1
        borrow.book.save()

        return borrow

    @staticmethod
    def check_overdue() -> int:
        updated = Borrow.objects.filter(
            due_date__lt=date.today(),
            status='BORROWED'
        ).update(status='LATE')
        return updated
