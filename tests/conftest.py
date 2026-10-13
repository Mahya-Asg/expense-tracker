import pytest

from expense_tracker.repository import InMemoryTransactionRepository
from expense_tracker.tracker import ExpenseTracker


@pytest.fixture
def repo():
    """Fresh in-memory repository for each test."""
    return InMemoryTransactionRepository()


@pytest.fixture
def tracker(repo):
    """Fresh ExpenseTracker instance for each test."""
    return ExpenseTracker(repo)