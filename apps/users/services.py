from .repositories import UserRepository
from .models import User


class UserService:

    @staticmethod
    def get_all():
        return UserRepository.get_all()

    @staticmethod
    def get_by_id(user_id: int):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def create(data: dict) -> User:
        return UserRepository.create(data)

    @staticmethod
    def update(user: User, data: dict) -> User:
        return UserRepository.update(user, data)

    @staticmethod
    def delete(user: User) -> None:
        UserRepository.delete(user)
