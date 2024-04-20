import pytest
import io
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController

@pytest.fixture
def user_controller():
    mock_dao = MagicMock()
    return UserController(dao=mock_dao)

def test_get_user_by_email_valid_email(user_controller):
    """ Mocking the result of returning a users infomation with only one user connected to one email"""
    user_controller.dao.find.return_value = [{'email': 'test@example.com', 'name': 'Test User'}]

    user = user_controller.get_user_by_email('test@example.com')

    assert user == user_controller.dao.find.return_value[0]

def test_get_user_by_email_invalid_email(user_controller):
    """ Testing get user infomation from an invalid email"""
    with pytest.raises(ValueError):
        user_controller.get_user_by_email('invalid_email')


def test_get_user_by_email_multiple_users(user_controller):
    """ Mocking the result of returning a users infomation with multiple user connected to one email """
    user_controller.dao.find.return_value = [{'email': 'test@example.com', 'name': 'Test User 1'},
                                             {'email': 'test@example.com', 'name': 'Test User 2'}]

    with patch('sys.stdout', new_callable=io.StringIO) as stdout_mock:
            user = user_controller.get_user_by_email('test@example.com')
            assert user == user_controller.dao.find.return_value[0]
            assert stdout_mock.getvalue() == 'Error: more than one user found with mail test@example.com\n'

def test_update(user_controller):
    user_controller.update = MagicMock(return_value=True)

    update_result = user_controller.update(123, {'name': 'Updated Name'})

    assert update_result == True

def test_get_user_by_email_valid_no_user(user_controller):
    """ Testing get user information from valid email with no users """
    with pytest.raises(TypeError):
        user_controller.dao.find.return_value = None
        user = user_controller.get_user_by_email('nouser@example.com')
        assert user == False
