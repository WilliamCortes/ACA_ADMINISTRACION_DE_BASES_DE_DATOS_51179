from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'book_id',
            'title',
            'author',
            'published_year',
            'stock',
            'description',
            'cover_url',
        ]
