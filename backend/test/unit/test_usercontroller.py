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
    user_controller.dao.find.return_value = ValueError
    with pytest.raises(ValueError):
        user_controller.get_user_by_email('invalid@email_invalid_')

def test_get_user_by_email_multiple_users(user_controller):
    """ Mocking the result of returning a users infomation with multiple user connected to one email """
    user_controller.dao.find.return_value = [{'email': 'test@example.com', 'name': 'Test User 1'},
                                             {'email': 'test@example.com', 'name': 'Test User 2'}]

    with patch('sys.stdout', new_callable=io.StringIO) as stdout_mock:
            user_controller.get_user_by_email('test@example.com')
            assert stdout_mock.getvalue() == 'Error: more than one user found with mail test@example.com\n'

@pytest.mark.unit
def test_get_user_by_email_valid_no_user(user_controller):
    """ Testing get user information from valid email with no users """
    user_controller.dao.find.return_value = None
    user = user_controller.get_user_by_email('nouser@example.com')
    assert user == None

@pytest.mark.unit
def test_get_user_by_email_database_failure_valid_email(user_controller):
     """ Testing failed database """
     user_controller.dao.find.return_value = Exception
     with pytest.raises(Exception):
          user_controller.get_user_by_email("exception@test.com")

@pytest.mark.unit
def test_get_user_by_email_database_failure_invalid_email(user_controller):
     """ Testing failed database """
     user_controller.dao.find.return_value = Exception
     with pytest.raises(Exception):
          user_controller.get_user_by_email("exception.test")
