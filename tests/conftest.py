"""Pytest configuration and fixtures."""
import pytest


@pytest.fixture
def sample_action():
    """Provide a sample action concept."""
    return "ACT.QUERY.DATA"


@pytest.fixture
def sample_target():
    """Provide a sample target concept."""
    return "ENT.DATA.TEXT"


@pytest.fixture
def sample_parameters():
    """Provide sample parameters."""
    return {"query": "test query", "limit": 10}
