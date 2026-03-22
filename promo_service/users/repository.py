from .models import User


class UserRepository:
    """Repository class for accessing user data."""

    @staticmethod
    def get_user(user_id: int) -> User | None:
        """Retrieves a user by their ID."""
        return User.objects.filter(id=user_id).first()
