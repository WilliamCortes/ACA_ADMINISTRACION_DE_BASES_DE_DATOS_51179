from .models import Borrow


class BorrowRepository:

    @staticmethod
    def get_all():
        return Borrow.objects.select_related('user', 'book').all()

    @staticmethod
    def get_by_id(borrow_id):
        return Borrow.objects.select_related('user', 'book').filter(borrow_id=borrow_id).first()

    @staticmethod
    def create(user_id: int, book_id: int, due_date) -> Borrow:
        return Borrow.objects.create(
            user_id=user_id,
            book_id=book_id,
            due_date=due_date,
            status='BORROWED',
        )

    @staticmethod
    def save(borrow: Borrow) -> Borrow:
        borrow.save()
        return borrow
