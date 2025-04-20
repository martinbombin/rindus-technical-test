"""Dependency injection utilities for FastAPI endpoints.

This module defines reusable dependencies, such as a SQLAlchemy session,
which can be injected into route handlers or services using FastAPI's `Depends`.

It provides:
- `get_session`: A generator-based dependency that yields a database session.
- `SessionDep`: A type alias for cleaner injection of SQLAlchemy sessions.
"""

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session


def get_session(request: Request):
    """Dependency that provides a scoped SQLAlchemy session.

    Opens a new session using the application's configured DB engine and ensures
    it's properly closed after the request is handled.

    Args:
        request (Request): The current FastAPI request, used to access app state.

    Yields:
        Session: A SQLAlchemy database session instance.

    """
    with Session(request.app.state.db_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
"""
Type alias for injecting a SQLAlchemy session using FastAPI's dependency system.

Usage:
    def endpoint(session: SessionDep):
        ...
"""
