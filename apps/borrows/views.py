from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import BorrowSerializer
from .services import BorrowService
from .repositories import BorrowRepository


class BorrowViewSet(viewsets.ViewSet):

    def list(self, request):
        borrows = BorrowRepository.get_all()
        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        borrow = BorrowRepository.get_by_id(pk)
        if borrow is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BorrowSerializer(borrow).data)

    @action(detail=False, methods=['post'], url_path='create_borrow')
    def create_borrow(self, request):
        user_id = request.data.get('user')
        book_id = request.data.get('book')
        due_date = request.data.get('due_date')

        if not all([user_id, book_id, due_date]):
            return Response(
                {'detail': 'Se requieren: user, book, due_date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            borrow = BorrowService.create_borrow(user_id, book_id, due_date)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='return_book')
    def return_book(self, request, pk=None):
        try:
            borrow = BorrowService.return_book(pk)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(BorrowSerializer(borrow).data)
