import pytest
import pymongo
from src.util.dao import DAO

@pytest.fixture
def dao():
    dao = DAO("task")
    yield dao
    dao.drop()

def test_create_all_correct(dao):
    """ Test valid data correct properties, bson and uniqueItems, returning object """
    task_dict = {'title': 'Unique', 'description': 'Description added'}
    expected_res = {'_id': {'$oid': ''}, 'title': 'Unique', 'description': 'Description added'}
    result = dao.create(task_dict)
    assert result.keys() == expected_res.keys()

def test_create_incorrect_properties(dao):
    """ Test valid data with incorrect properties, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        task_dict = {'title': 'Title'}
        result = dao.create(task_dict)
        assert result == Exception

def test_create_incorrect_bson(dao):
    """ Test valid data with incorrect bson type, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        task_dict = {'title': 1, 'description': 'Description added'}
        result = dao.create(task_dict)
        assert result == Exception

def test_create_incorrect_uniqueItems(dao):
    """ Test valid data with incorrect unique items, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        task_dict = {'title': 'Not unique', 'description': 'Description added'}
        dao.create(task_dict)
        result = dao.create(task_dict)
        assert result == Exception

def test_create_invalid_data(dao):
    """ Test invalid data, raising Exception """
    with pytest.raises(Exception):
        dict = "invalid" 
        result = dao.create(dict)
        assert result == Exception