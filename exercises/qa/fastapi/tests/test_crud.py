import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app import crud, models, schemas


@patch('app.database.get_db')
def test_when_get_task_that_exists_then_task_is_returned(mock_get_db):
    
    mock_task = MagicMock()
    mock_task = models.Task(id=1, title="Test Task", description="Test Description")

    mock_get_db.return_value.__next__.return_value.query.return_value.filter.return_value.first.return_value = mock_task

    # Call the function under test
    result = crud.get_task(1)

    # Assertions
    assert result.id == mock_task.id  # Compare relevant attributes
    assert result.title == mock_task.title
    assert result.description == mock_task.description

@patch('app.database.get_db')
def test_when_get_task_that_does_not_exist_then_HtppException_is_thrown(mock_get_db):
    
    mock_task = MagicMock()
    mock_task = None

    mock_get_db.return_value.__next__.return_value.query.return_value.filter.return_value.first.return_value = mock_task

    # Call the function under test
    with pytest.raises(HTTPException) as exc_info:
        result = crud.get_task(1)

    # Assert that the exception has the expected status code and detail
    assert exc_info.value.status_code == 400
    assert "Task not found" in str(exc_info.value.detail)


@patch('app.database.get_db')
def test_when_creating_task_with_short_title_then_HtppException_is_thrown(mock_get_db):
    
    mock_task = MagicMock()
    mock_task = None

    mock_get_db.return_value.__next__.return_value.query.return_value.filter.return_value.first.return_value = mock_task

    task_create = schemas.TaskCreate(
        title = "sho",
        description = "proper_description",
        completed=False
    )

    # Call the function under test
    with pytest.raises(HTTPException) as exc_info:
        result = crud.create_task(task_create)

    # Assert that the exception has the expected status code and detail
    assert exc_info.value.status_code == 400
    assert "Title length" in str(exc_info.value.detail)

    # Assert that query() is not called in the DB
    mock_get_db.return_value.__next__.return_value.query.assert_not_called()

@patch('app.database.get_db')
def test_when_creating_task_then_task_is_created(mock_get_db):
    
    mock_task = MagicMock()
    mock_task = None

    mock_get_db.return_value.__next__.return_value.query.return_value.filter.return_value.first.return_value = mock_task

    task_create = schemas.TaskCreate(
        title = "proper_title",
        description = "proper_description",
        completed=False
    )

    # Call the function under test
    result = crud.create_task(task_create)

    # Assert that methods are called in the DB
    mock_get_db.return_value.__next__.return_value.add.assert_called_once()
    mock_get_db.return_value.__next__.return_value.commit.assert_called_once()
    mock_get_db.return_value.__next__.return_value.refresh.assert_called_once()

    added_task = mock_get_db.return_value.__next__.return_value.add.call_args[0][0]

    # Assert that the values added to the DB are the expected ones
    assert added_task.title == task_create.title
    assert added_task.description == task_create.description
    assert added_task.completed == task_create.completed

    # Assert that the task returned by the method is the expected one
    assert result.title == task_create.title
    assert result.description == task_create.description
    assert result.completed == task_create.completed
