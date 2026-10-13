from datetime import datetime
from decimal import Decimal

from expense_tracker.json_repository import JSONTransactionRepository
from expense_tracker.models import Category, Transaction, TransactionType
from expense_tracker.tracker import ExpenseTracker


def test_new_repository_starts_empty(json_repo_with_path):
    repo, _ = json_repo_with_path
    assert repo.get_all() == []


def test_add_and_load_transaction(json_repo_with_path):
    repo, file_path = json_repo_with_path

    transaction = Transaction(
        id=0,
        amount=Decimal("1500"),
        type=TransactionType.EXPENSE,
        category=Category("Rent"),
        date=datetime(2026, 10, 1, 12, 0, 0),
        description="Apartment rent"
    )
    repo.add(transaction)
    
    # Reload from the same file
    repo2 = JSONTransactionRepository(str(file_path))
    loaded = repo2.get_all()

    assert len(loaded) == 1
    assert loaded[0].amount == Decimal("1500")
    assert loaded[0].category.name == "Rent"
    assert loaded[0].description == "Apartment rent"

def test_multiple_transactions_are_persisted(json_repo_with_path):
    repo, file_path = json_repo_with_path

    t1 = Transaction(
        id=0,
        amount=Decimal("5000"),
        type=TransactionType.INCOME,
        category=Category("Salary"),
        date=datetime(2026, 10, 1),
        description="Salary"
    )
    t2 = Transaction(
        id=0,
        amount=Decimal("200"),
        type=TransactionType.EXPENSE,
        category=Category("Food"),
        date=datetime(2026, 10, 2),
        description="Lunch"
    )

    repo.add(t1)
    repo.add(t2)

    repo2 = JSONTransactionRepository(str(file_path))
    loaded = repo2.get_all()

    assert len(loaded) == 2
    assert loaded[0].amount == Decimal("5000")
    assert loaded[1].amount == Decimal("200")


def test_ids_are_assigned_correctly(json_repo_with_path):
    repo, _ = json_repo_with_path

    t1 = Transaction(
        id=0,
        amount=Decimal("100"),
        type=TransactionType.EXPENSE,
        category=Category("Food"),
        date=datetime.now()
    )
    t2 = Transaction(
        id=0,
        amount=Decimal("200"),
        type=TransactionType.EXPENSE,
        category=Category("Transport"),
        date=datetime.now()
    )

    repo.add(t1)
    repo.add(t2)

    loaded = repo.get_all()
    assert loaded[0].id == 1
    assert loaded[1].id == 2



def test_invalid_data_in_file_is_skipped(json_repo_with_path):
    """Invalid transactions in the JSONL file should be skipped."""
    _, file_path = json_repo_with_path

    # Manually write one valid and one invalid line
    file_path.write_text(
        '{"id": 1, "amount": "100.00", "type": "expense", "category": "Food", '
        '"date": "2026-10-01T10:00:00", "description": "Lunch", "tags": null}\n'
        '{"id": 2, "amount": "-50.00", "type": "expense", "category": "Food", '
        '"date": "2026-10-01T11:00:00", "description": "Bad", "tags": null}\n',
        encoding="utf-8"
    )

    # Reload from the same file
    repo2 = JSONTransactionRepository(str(file_path))
    loaded = repo2.get_all()

    assert len(loaded) == 1
    assert loaded[0].amount == Decimal("100.00")
    assert loaded[0].category.name == "Food"


def test_empty_and_corrupted_lines_do_not_crash(json_repo_with_path):
    """Empty lines and corrupted JSON should not crash the repository."""
    _, file_path = json_repo_with_path

    file_path.write_text(
        "\n"
        "this is not json\n"
        '{"id": 1, "amount": "200.00", "type": "income", "category": "Salary", '
        '"date": "2026-10-01T09:00:00", "description": "Pay", "tags": null}\n'
        "\n"
        "{broken json\n",
        encoding="utf-8"
    )

    repo2 = JSONTransactionRepository(str(file_path))
    loaded = repo2.get_all()

    assert len(loaded) == 1
    assert loaded[0].amount == Decimal("200.00")
    assert loaded[0].type == TransactionType.INCOME


def test_balance_is_recalculated_after_loading(json_repo_with_path):
    """Tracker should recalculate balance correctly after loading from file."""
    repo, file_path = json_repo_with_path

    t1 = Transaction(
        id=0,
        amount=Decimal("5000"),
        type=TransactionType.INCOME,
        category=Category("Salary"),
        date=datetime(2026, 10, 1),
        description="Salary"
    )
    t2 = Transaction(
        id=0,
        amount=Decimal("1500"),
        type=TransactionType.EXPENSE,
        category=Category("Rent"),
        date=datetime(2026, 10, 2),
        description="Rent"
    )

    repo.add(t1)
    repo.add(t2)

    # New repository + tracker loading from the same file
    repo2 = JSONTransactionRepository(str(file_path))
    tracker = ExpenseTracker(repo2)

    assert tracker.get_balance() == Decimal("3500")
    assert tracker.get_total_income() == Decimal("5000")
    assert tracker.get_total_expense() == Decimal("1500")

