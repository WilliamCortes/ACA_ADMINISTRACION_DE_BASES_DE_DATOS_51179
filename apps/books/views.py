from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .services import BookService


class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        books = BookService.get_all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = BookService.create(serializer.validated_data)
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        book = BookService.get_by_id(pk)
        if book is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BookSerializer(book).data)

    def update(self, request, pk=None):
        book = BookService.get_by_id(pk)
        if book is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = BookService.update(book, serializer.validated_data)
        return Response(BookSerializer(updated).data)

    def destroy(self, request, pk=None):
        book = BookService.get_by_id(pk)
        if book is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        BookService.delete(book)
        return Response(status=status.HTTP_204_NO_CONTENT)
