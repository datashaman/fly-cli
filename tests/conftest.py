import pytest
from fly_cli import FlyCLI


@pytest.fixture
def fly():
    return FlyCLI()
