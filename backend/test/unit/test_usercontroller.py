import pytest

from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController


@pytest.fixture
def usercontroller():
    mock_dao = MagicMock()
    return UserController(dao=mock_dao)

class TestUserController:
    def test_NoneEmail(self):
        """ Testing the return of an empty string """
        with pytest.raises(ValueError):
            UserController.get_user_by_email(self, "")

    def test_invalidEmail(self):
        """ Testing an email that do not match the emailValidator requirements """
        with pytest.raises(ValueError):
            UserController.get_user_by_email(self, "Test")

    def test_validEmailNotUsed(self):
        """ Testing an email that is valid and not in use """
        with pytest.raises(Exception):
            UserController.get_user_by_email(self, 'Test@valid.com')

    def test_validEmailUsed(self):
        """ Testing an email that is valid and not in use """
       



