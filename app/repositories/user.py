"""User repository module for handling database interactions related to the User model.

This module provides the `UserRepository` class, which abstracts CRUD operations
and query utilities for users in a SQLAlchemy-backed database.
"""

import uuid

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app import models


class UserRepository:
    """Repository class for performing database operations on User objects.

    Attributes:
        session (Session): SQLAlchemy session used for database interactions.

    """

    def __init__(self, session: Session) -> None:
        """Initialize the UserRepository with a database session.

        Args:
            session (Session): The SQLAlchemy session to use.

        """
        self.session = session

    def user_exists(self, email: str) -> bool:
        """Check whether a user with the given email exists in the database.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if a user with the email exists, False otherwise.

        """
        return self.session.query(
            exists().where(models.User.email == email),
        ).scalar()

    def create_user(self, user: models.User) -> models.User:
        """Create a new user in the database.

        Args:
            user (models.User): The User object to add.

        Returns:
            models.User: The newly created and refreshed User object.

        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_users(
        self,
        offset: int = 0,
        limit: int = 100,
        username: str | None = None,
        email: str | None = None,
    ) -> list[models.User]:
        """Retrieve a list of users from the database, with optional filters.

        Args:
            offset (int): The starting index for pagination. Default is 0.
            limit (int): The maximum number of users to return. Default is 100.
            username (str | None): Optional filter by username.
            email (str | None): Optional filter by email.

        Returns:
            list[models.User]: A list of User objects matching the criteria.

        """
        stmt = select(models.User)

        if username:
            stmt = stmt.where(models.User.username == username)
        if email:
            stmt = stmt.where(models.User.email == email)

        stmt = stmt.offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_user_by_id(self, user_id: uuid.UUID) -> models.User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id (uuid.UUID): The UUID of the user to retrieve.

        Returns:
            models.User | None: The User object if found, or None if not found.

        """
        return self.session.get(models.User, str(user_id))
