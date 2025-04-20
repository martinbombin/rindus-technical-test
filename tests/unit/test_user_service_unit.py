import uuid
from unittest.mock import MagicMock, patch

import pytest

from app import exceptions
from app.services.user import (
    create_user_in_db,
    get_user_by_id,
    get_users_from_db,
)


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.mark.unit
def test_create_user_success(user_create, mock_repo):
    fake_user = MagicMock(
        email=user_create.email,
        username=user_create.username,
    )
    mock_repo.user_exists.return_value = False
    mock_repo.create_user.return_value = fake_user

    with patch(
        "app.services.user.UserRepository",
        return_value=mock_repo,
    ):
        result = create_user_in_db(
            session=MagicMock(),
            user_create=user_create,
        )

    assert result.email == user_create.email
    assert result.username == user_create.username
    mock_repo.create_user.assert_called_once()


@pytest.mark.unit
def test_create_user_with_existing_email_raises(user_create, mock_repo):
    mock_repo.user_exists.return_value = True

    with (
        patch(
            "app.services.user.UserRepository",
            return_value=mock_repo,
        ),
        pytest.raises(exceptions.ExistingEmailError),
    ):
        create_user_in_db(
            session=MagicMock(),
            user_create=user_create,
        )

    mock_repo.create_user.assert_not_called()


@pytest.mark.unit
def test_get_users_from_db_basic(mock_repo):
    mock_users = [MagicMock(id="1"), MagicMock(id="2")]
    mock_repo.get_users.return_value = mock_users

    with patch(
        "app.services.user.UserRepository",
        return_value=mock_repo,
    ):
        result = get_users_from_db(session=MagicMock())

    assert result == mock_users
    mock_repo.get_users.assert_called_once()


@pytest.mark.unit
def test_get_users_from_db_with_filters(mock_repo):
    filtered_users = [MagicMock(id="1", username="filtered_user")]
    mock_repo.get_users.return_value = filtered_users

    with patch(
        "app.services.user.UserRepository",
        return_value=mock_repo,
    ):
        result = get_users_from_db(
            session=MagicMock(),
            username="filtered_user",
            email="filtered@example.com",
            offset=1,
            limit=10,
        )

    assert result == filtered_users
    mock_repo.get_users.assert_called_once_with(
        offset=1,
        limit=10,
        username="filtered_user",
        email="filtered@example.com",
    )


@pytest.mark.unit
def test_get_user_by_id_found(mock_repo):
    user_id = uuid.uuid4()
    fake_user = MagicMock(id=str(user_id))
    mock_repo.get_user_by_id.return_value = fake_user

    with patch(
        "app.services.user.UserRepository",
        return_value=mock_repo,
    ):
        result = get_user_by_id(session=MagicMock(), user_id=user_id)

    assert result == fake_user
    mock_repo.get_user_by_id.assert_called_once_with(user_id)


@pytest.mark.unit
def test_get_user_by_id_not_found(mock_repo):
    user_id = uuid.uuid4()
    mock_repo.get_user_by_id.return_value = None

    with patch(
        "app.services.user.UserRepository",
        return_value=mock_repo,
    ):
        result = get_user_by_id(session=MagicMock(), user_id=user_id)

    assert result is None
    mock_repo.get_user_by_id.assert_called_once_with(user_id)
