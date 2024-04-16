import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO

#allowing interaction with the database without disturbing production code or data
@pytest.fixture



# Not correct yet!
def test_create_task_not_violated():
    """ Test data matching task and not violating validators, returning object """
    # task_dict = {'title': 'Unique', 'description': 'Description added'}
    # dao_task = DAO("task")
    # result = dao_task.create(task_dict)
    # assert result == {'_id': 1, 'title': 'Unique', 'description': 'Description added'}

def test_create_task_violated():
    """ Test data matching task and violating validators, WriteError """
    task_dict = {'title': 'Title'}

def test_create_todo_not_violated():
    """ Test data matching todo and not violating validators, returning object """

def test_create_todo_violated():
    """ Test data matching todo and violating validators, WriteError """

def test_create_user_not_violated():
    """ Test data matching user and not violating validators, returning object """

def test_create_user_violated():
    """ Test data matching user and violating validators, WriteError """

def test_create_video_not_violated():
    """ Test data matching video and not violating validators, returning object """

def test_create_video_violated():
    """ Test data matching video and violating validators, WriteError """

def test_create_no_match_violated():
    """ Test data with no match and therefore violating validators, Exception """