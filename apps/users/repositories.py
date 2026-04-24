from .models import User


class UserRepository:

    @staticmethod
    def get_all():
        return User.objects.all()

    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(user_id=user_id).first()

    @staticmethod
    def create(data: dict) -> User:
        return User.objects.create(**data)

    @staticmethod
    def update(user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def delete(user: User) -> None:
        user.delete()
