from .repositories import BookRepository
from .models import Book


class BookService:

    @staticmethod
    def get_all():
        return BookRepository.get_all()

    @staticmethod
    def get_by_id(book_id: int):
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def create(data: dict) -> Book:
        return BookRepository.create(data)

    @staticmethod
    def update(book: Book, data: dict) -> Book:
        return BookRepository.update(book, data)

    @staticmethod
    def delete(book: Book) -> None:
        BookRepository.delete(book)

    @staticmethod
    def get_cover_url(isbn: str) -> str:
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
