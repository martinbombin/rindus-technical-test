"""User service layer for encapsulating business logic related to user operations.

This module acts as a bridge between the API layer and the repository layer,
handling application-specific concerns like checking for existing users or
transforming schema data into model instances.
"""

import uuid

from passlib.context import CryptContext

from app import dependencies, exceptions, models
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


def create_user_in_db(
    session: dependencies.SessionDep,
    user_create: schemas_user.UserCreate,
) -> models.User:
    """Create a new user in the database after validating uniqueness.

    Args:
        session (SessionDep): The SQLAlchemy session dependency.
        user_create (UserCreate): The user creation schema with input data.

    Raises:
        ExistingEmailError: If a user with the same email already exists.

    Returns:
        models.User: The newly created User ORM model.

    """
    repo = UserRepository(session)

    if repo.user_exists(user_create.email):
        raise exceptions.ExistingEmailError

    hashed_password = hash_password(
        user_create.password,
    )
    user_create.password = hashed_password
    user = models.User(**user_create.model_dump())

    return repo.create_user(user)


def get_users_from_db(
    session: dependencies.SessionDep,
    offset: int = 0,
    limit: int = 100,
    username: str | None = None,
    email: str | None = None,
) -> list[models.User]:
    """Retrieve a list of users from the database with optional filters.

    Args:
        session (SessionDep): The SQLAlchemy session dependency.
        offset (int): Pagination offset. Default is 0.
        limit (int): Maximum number of users to return. Default is 100.
        username (str | None): Optional filter by username.
        email (str | None): Optional filter by email.

    Returns:
        list[models.User]: A list of User ORM models matching the query.

    """
    repo = UserRepository(session)
    return repo.get_users(
        offset=offset,
        limit=limit,
        username=username,
        email=email,
    )


def get_user_by_id(
    session: dependencies.SessionDep,
    user_id: uuid.UUID,
) -> models.User | None:
    """Retrieve a single user by their UUID.

    Args:
        session (SessionDep): The SQLAlchemy session dependency.
        user_id (uuid.UUID): The unique identifier of the user.

    Returns:
        models.User | None: The user object if found, or None if not found.

    """
    repo = UserRepository(session)
    return repo.get_user_by_id(user_id)
