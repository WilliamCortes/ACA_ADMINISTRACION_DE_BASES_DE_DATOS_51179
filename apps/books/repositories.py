from .models import Book


class BookRepository:

    @staticmethod
    def get_all():
        return Book.objects.all()

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.filter(book_id=book_id).first()

    @staticmethod
    def create(data: dict) -> Book:
        return Book.objects.create(**data)

    @staticmethod
    def update(book: Book, data: dict) -> Book:
        for field, value in data.items():
            setattr(book, field, value)
        book.save()
        return book

    @staticmethod
    def delete(book: Book) -> None:
        book.delete()
