import pytest
import pymongo
from unittest.mock import patch
from src.util.dao import DAO

@pytest.fixture
@patch('src.util.dao.getValidator')
def dao(mock_getValidator):
    mock_getValidator.return_value = {
    "$jsonSchema": { "bsonType": "object",
        "required": ["title", "description"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "the title of a task must be determined",
                "uniqueItems": True
            }, 
            "description": {
                "bsonType": "string",
                "description": "the description of a task must be determined"
            }}}}
    dao = DAO("test")
    return dao

def test_create_all_correct(dao):
    """ Test valid data correct properties, bson and uniqueItems, returning object """
    test_dict = {'title': 'Unique', 'description': 'Description added'}
    expected_res = {'_id': {'$oid': ''}, 'title': 'Unique', 'description': 'Description added'}
    result = dao.create(test_dict)
    assert result.keys() == expected_res.keys()

def test_create_incorrect_properties(dao):
    """ Test valid data with incorrect properties, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        test_dict = {'title': 'Title'}
        result = dao.create(test_dict)
        assert result == Exception

def test_create_incorrect_bson(dao):
    """ Test valid data with incorrect bson type, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        test_dict = {'title': 1, 'description': 'Description added'}
        result = dao.create(test_dict)
        assert result == Exception

def test_create_incorrect_uniqueItems(dao):
    """ Test valid data with incorrect unique items, raising WriteError """
    with pytest.raises(pymongo.errors.WriteError):
        test_dict = {'title': 'Not unique', 'description': 'Description added'}
        dao.create(test_dict)
        result = dao.create(test_dict)
        assert result == Exception

def test_create_invalid_data(dao):
    """ Test invalid data, raising Exception """
    with pytest.raises(Exception):
        test_dict = "invalid" 
        result = dao.create(test_dict)
        assert result == Exception