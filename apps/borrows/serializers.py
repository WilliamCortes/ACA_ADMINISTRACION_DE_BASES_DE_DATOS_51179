from rest_framework import serializers
from .models import Borrow


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = [
            'borrow_id',
            'user',
            'book',
            'borrow_date',
            'due_date',
            'return_date',
            'status',
        ]
        read_only_fields = ['borrow_id', 'borrow_date', 'return_date', 'status']
