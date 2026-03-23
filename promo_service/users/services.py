from rest_framework.exceptions import ValidationError

from users.repository import UserRepository


class UserService:
    """Service for user operations."""

    @staticmethod
    def get_user(user_id: int):
        """
        Retrieves a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to retrieve.

        Returns
        -------
        User | None
            The user instance if found, otherwise None.
        """
        user = UserRepository.get_user(user_id)
        if not user:
            raise ValidationError("Пользователь не найден")
        return user
