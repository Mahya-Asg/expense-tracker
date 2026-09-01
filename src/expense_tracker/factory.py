from datetime import datetime
from decimal import Decimal

from .models import Transaction, TransactionType, Category

class TransactionFactory():
    @staticmethod
    def create_income(amount: Decimal,
                    category: Category,
                    description: str == "",
                    tags: tuple[str, ...] | None = None) -> Transaction:
        return Transaction(id = 0,  
                        amount = amount,
                        type = TransactionType.INCOME,
                        date= datetime.now(),
                        category= category,
                        description= description,
                        tags= tags)

    @staticmethod
    def create_expense(amount: Decimal,
                    category: Category,
                    description: str == "",
                    tags: Optional[Tuple[str, ...]] = None) -> Transaction:

        return Transaction(id = 0,
                        amount = amount,
                        type = TransactionType.EXPENSE,
                        date= datetime.now(),
                        category= category,
                        description= description,
                        tags= tags)