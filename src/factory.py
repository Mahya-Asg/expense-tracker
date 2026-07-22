from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from models import Transaction, TransactionType, Category

class TransactionFactory():
    @staticmethod
    def create_income(amount: Decimal,
                    category: Category,
                    description: str == "",
                    tags: Optional(Tuple[str, ...]) = None) -> Transaction:
        return Transaction(id = 0,
                        amount = amount,
                        type = TransactionType.INCOME,
                        date= datetime.now(),
                        category= category,
                        description= description,
                        tags= tags)

    @staticmethod
    def create_expence(amount: Decimal,
                    category: Category,
                    description: str == "",
                    tags: Optional(Tuple[str, ...]) = None) -> Transaction:

        return Transaction(id = 0,
                        amount = amount,
                        type = TransactionType.EXPENSE,
                        date= datetime.now(),
                        category= category,
                        description= description,
                        tags= tags)