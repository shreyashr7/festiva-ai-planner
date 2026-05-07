"""Test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_event():
    """Sample event data for testing."""
    return {
        "event_type": "Wedding",
        "guest_count": 500,
        "total_budget": 2500000,
        "event_month": 5,
        "location": "Bengaluru",
    }
