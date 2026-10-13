import pytest

from expense_tracker.json_repository import JSONTransactionRepository
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


@pytest.fixture
def json_repo_with_path(tmp_path):
    """
    Returns both the repository and the temporary file path.
    Useful when we need to reload data from the same file.
    """
    file_path = tmp_path / "test_transaction.jsonl"
    repo = JSONTransactionRepository(file_path)
    return repo, file_path
