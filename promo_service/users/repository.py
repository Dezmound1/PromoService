from .models import User


class UserRepository:
    """Repository class for accessing user data."""

    @staticmethod
    def get_user(user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to retrieve.

        Returns
        -------
        User | None
            The user instance if found, otherwise None.
        """
        return User.objects.filter(id=user_id).first()
