"""FastAPI application setup and startup configuration.

This module initializes the FastAPI app, configures the database connection,
creates database tables at startup, and includes API routers.

Key components:
- `lifespan`: Async context manager that sets up the database engine on app startup.
- `create_db_and_tables`: Initializes database schema from ORM models.
- `app`: The FastAPI instance with registered routes and lifecycle management.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine
from sqlalchemy.engine import URL, create_engine

from app import config, models
from app.routers import user as users_router


def create_db_and_tables(engine: Engine) -> None:
    """Create all tables defined in the ORM models if they don't already exist.

    Args:
        engine (Engine): SQLAlchemy engine used to connect to the database.

    """
    models.Base.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager to set up and tear down application resources.

    This function initializes the SQLAlchemy engine using environment configuration
    and attaches it to the FastAPI app's state. Tables are created on startup.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Keeps the app running while the context is active.

    """
    url_object = URL.create(
        config.settings.db_type,
        username=config.settings.db_user,
        password=config.settings.db_password,
        host=config.settings.db_host,
        port=config.settings.db_port,
        database=config.settings.db_name,
    )
    engine = create_engine(url_object, echo=True)

    create_db_and_tables(engine=engine)
    app.state.db_engine = engine
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router.router)
