from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple # pay ATTENTION !!!


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True)
class Category:
    name: str

@dataclass(frozen=True)
class Transaction:
    id: int
    amount: Decimal
    type: TransactionType
    category: Category

    date: datetime
    description: str == ""
    tags: Optional(Tuple[str, ...]) = None # pay ATTENTION !!!



