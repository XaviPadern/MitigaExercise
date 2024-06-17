from exercises.qa.fastapi.app import main

import pytest
from typing import Generator
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Provides a test client for the application."""
    
    with TestClient(main.app) as test_client:
        yield test_client