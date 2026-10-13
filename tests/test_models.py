from dataclasses import FrozenInstanceError
from datetime import datetime
from decimal import Decimal

import pytest

from expense_tracker.exceptions import InvalidTransactionError
from expense_tracker.models import Category, Transaction, TransactionType


def test_create_valid_category():
    category = Category("Food")
    assert category.name == "Food"

def test_category_strips_spaces():
    category = Category("  Transport ")
    assert category.name == "Transport"

def test_empty_category_raises_error():
    with pytest.raises(InvalidTransactionError):
        Category("")


def test_category_with_only_spaces_raises_error():
    with pytest.raises(InvalidTransactionError):
        Category("      ")

def test_create_valid_transaction():
    category = Category("Salary")
    transaction = Transaction(
        id=1,
        amount=Decimal("5000"),
        type=TransactionType.INCOME,
        category=category,
        date=datetime.now(),
        description="Monthly salary"
    )
    assert transaction.amount == Decimal("5000")
    assert transaction.category.name == "Salary"

def test_negative_amount_raises_error():
    category = Category("Food")
    with pytest.raises(InvalidTransactionError):
        Transaction(
            id=1,
            amount=Decimal("-100"),
            type=TransactionType.EXPENSE,
            category=category,
            date=datetime.now()
        )


def test_zero_amount_raises_error():
    category = Category("Food")
    with pytest.raises(InvalidTransactionError):
        Transaction(
            id=1,
            amount=Decimal("0"),
            type=TransactionType.EXPENSE,
            category=category,
            date=datetime.now()
        )


def test_description_is_stripped():
    category = Category("Food")
    transaction = Transaction(
        id=1,
        amount=Decimal(50),
        type=TransactionType.EXPENSE,
        category=category,
        date=datetime.now(),
        description="   Lunch  ",    
    )   
    assert transaction.description == "Lunch"


def test_long_description_raises_error():
    category = Category("Food")
    long_description = "a" * 256  # 256 characters

    with pytest.raises(InvalidTransactionError):
        Transaction(
            id=1,
            amount=Decimal("50"),
            type=TransactionType.EXPENSE,
            category=category,
            date=datetime.now(),
            description=long_description
        )

def test_transaction_is_frozen():
    category = Category("Food")
    transaction = Transaction(
        id=1,
        amount=Decimal("50"),
        type=TransactionType.EXPENSE,
        category=category,
        date=datetime.now()
    )

    with pytest.raises(FrozenInstanceError) as exc_info:  # FrozenInstanceError
        transaction.amount = Decimal("100")

    # print(exc_info.value)           # cannot assign to field 'amount'
    # print(exc_info.type)            # <class 'dataclasses.FrozenInstanceError'>
    assert str(exc_info.value) == "cannot assign to field 'amount'"

