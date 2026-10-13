from decimal import Decimal

import pytest

from expense_tracker.exceptions import InvalidTransactionError
from expense_tracker.models import Category


def test_initial_balance_is_zero(tracker):
    assert tracker.get_balance() == Decimal("0")  
    assert tracker.get_total_income() == Decimal("0")
    assert tracker.get_total_expense() == Decimal("0")


def test_add_income_increases_balance(tracker):
    tracker.add_income(Decimal("5000"), Category("Salary"), "Monthly salary")

    assert tracker.get_balance() == Decimal("5000")
    assert tracker.get_total_income() == Decimal("5000")
    assert tracker.get_total_expense() == Decimal("0")


def test_add_expense_decreases_balance(tracker):
    tracker.add_income(Decimal("5000"), Category("Salary"))
    tracker.add_expense(Decimal("1500"), Category("Rent"), "Apartment rent")

    assert tracker.get_balance() == Decimal("3500")
    assert tracker.get_total_income() == Decimal("5000")
    assert tracker.get_total_expense() == Decimal("1500")


def test_multiple_transactions(tracker):
    tracker.add_income(Decimal("6000"), Category("Salary"))
    tracker.add_expense(Decimal("2000"), Category("Rent"))
    tracker.add_expense(Decimal("500"), Category("Food"))
    tracker.add_income(Decimal("1000"), Category("Freelance"))

    assert tracker.get_balance() == Decimal("4500")
    assert tracker.get_total_income() == Decimal("7000")
    assert tracker.get_total_expense() == Decimal("2500")


def test_invalid_amount_is_rejected(tracker):
    with pytest.raises(InvalidTransactionError):
        tracker.add_expense(Decimal("-100"), Category("Food"))


def test_empty_category_is_rejected(tracker):
    with pytest.raises(InvalidTransactionError):
        tracker.add_expense(Decimal("50"), Category(""))


def test_transactions_are_stored(tracker, repo):
    tracker.add_income(Decimal("3000"), Category("Salary"), "Test income")
    tracker.add_expense(Decimal("200"), Category("Food"), "Lunch")

    transactions = repo.get_all()

    assert len(transactions) == 2
    assert transactions[0].amount == Decimal("3000")
    assert transactions[0].category.name == "Salary"
    assert transactions[1].amount == Decimal("200")
    assert transactions[1].category.name == "Food"