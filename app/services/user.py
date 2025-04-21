"""User service layer for encapsulating business logic related to user operations.

This module acts as a bridge between the API layer and the repository layer,
handling application-specific concerns like checking for existing users or
transforming schema data into model instances.

Key components:
- `UserService`: Class encapsulating user-related operations.
"""

import uuid

from passlib.context import CryptContext

from app import exceptions, models
from app.repositories.user import UserRepository
from app.schemas import user as schemas_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.

    """
    return pwd_context.hash(password)


class UserService:
    """Service class responsible for user-related business logic."""

    def __init__(self, user_repo: UserRepository) -> None:
        """Initialize the UserService.

        Args:
            user_repo (UserRepository): The user repository instance used for database operations.

        """
        self.user_repo = user_repo

    def create_user_in_db(
        self,
        user_create: schemas_user.UserCreate,
    ) -> models.User:
        """Create a new user in the database after validating uniqueness.

        Args:
            user_create (UserCreate): The user creation schema with input data.

        Raises:
            ExistingEmailError: If a user with the same email already exists.

        Returns:
            models.User: The newly created User ORM model.

        """
        if self.user_repo.user_exists(user_create.email):
            raise exceptions.ExistingEmailError

        hashed_password = hash_password(
            user_create.password,
        )
        user_create.password = hashed_password
        user = models.User(**user_create.model_dump())

        return self.user_repo.create_user(user)

    def get_users_from_db(
        self,
        offset: int = 0,
        limit: int = 100,
        username: str | None = None,
        email: str | None = None,
    ) -> list[models.User]:
        """Retrieve a list of users from the database with optional filters.

        Args:
            offset (int): Pagination offset. Default is 0.
            limit (int): Maximum number of users to return. Default is 100.
            username (str | None): Optional filter by username.
            email (str | None): Optional filter by email.

        Returns:
            list[models.User]: A list of User ORM models matching the query.

        """
        return self.user_repo.get_users(
            offset=offset,
            limit=limit,
            username=username,
            email=email,
        )

    def get_user_by_id(
        self,
        user_id: uuid.UUID,
    ) -> models.User | None:
        """Retrieve a single user by their UUID.

        Args:
            user_id (uuid.UUID): The unique identifier of the user.

        Returns:
            models.User | None: The user object if found, or None if not found.

        """
        return self.user_repo.get_user_by_id(user_id)
