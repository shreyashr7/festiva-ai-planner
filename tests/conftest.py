"""Test fixtures and shared configuration."""

import pytest


@pytest.fixture
def sample_event():
    """Sample event request data."""
    return {
        "event_type": "Wedding",
        "guest_count": 500,
        "total_budget": 2500000,
        "event_month": 5,
        "location": "Bengaluru",
    }


@pytest.fixture
def sample_budget_request():
    """Sample budget prediction request."""
    return {
        "event_type": "Corporate",
        "guest_count": 300,
        "total_budget": 1500000,
        "event_month": 8,
    }
