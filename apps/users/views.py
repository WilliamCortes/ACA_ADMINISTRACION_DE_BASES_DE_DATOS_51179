from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .services import UserService


class UserViewSet(viewsets.ViewSet):

    @extend_schema(responses=UserSerializer(many=True))
    def list(self, request):
        users = UserService.get_all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, responses={201: UserSerializer})
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=UserSerializer)
    def retrieve(self, request, pk=None):
        user = UserService.get_by_id(pk)
        if user is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def update(self, request, pk=None):
        user = UserService.get_by_id(pk)
        if user is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = UserService.update(user, serializer.validated_data)
        return Response(UserSerializer(updated).data)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None):
        user = UserService.get_by_id(pk)
        if user is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        UserService.delete(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
