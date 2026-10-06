from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional # pay ATTENTION !!!

from .exceptions import InvalidTransactionError


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True)
class Category:
    name: str
    def __post_init__(self):
        cleaned_name = self.name.strip()

        if not cleaned_name:
            raise InvalidTransactionError("Category name cannot be empty.")

        # Because the dataclass is frozen, we use object.__setattr__
        object.__setattr__(self, "name", cleaned_name)

@dataclass(frozen=True)
class Transaction:
    id: int
    amount: Decimal
    type: TransactionType
    category: Category
    date: datetime
    description: str == ""
    tags: Optional[tuple[str, ...]] = None # pay ATTENTION !!!

    def __post_init__(self):
        # 1. Validate amount
        if self.amount <= 0:
            raise InvalidTransactionError("Amount must be greater than zero.")

        # 2. Validate description length
        if len(self.description) > 255:
            raise InvalidTransactionError("Description cannot be longer than 255 characters.")

        # 3. Clean the description
        cleaned_description = self.description.strip()
        object.__setattr__(self, "description", cleaned_description)




