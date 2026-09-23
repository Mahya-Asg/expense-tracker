from decimal import Decimal
from typing import Optional

from .models import Transaction, TransactionType, Category
from .repository import TransactionsRepository
from .factory import TransactionFactory
from .report import ReportGenerator



class ExpenseTracker():
    def __init__(self, repository: TransactionsRepository, factory:Optional[TransactionFactory]=None):
        self.repository = repository
        self.factory = factory or TransactionFactory()


       # Initialize and calculate totals from existing data
        self._recalculate_totals()

    def _recalculate_totals(self):
        """
        Recalculate running balance, total income and total expense
        based on all transactions currently in the repository.
        """
        self._balance: Decimal = Decimal('0')
        self._total_income: Decimal = Decimal('0')
        self._total_expense: Decimal = Decimal('0')
        for transaction in self.repository.get_all():
            if transaction.type == TransactionType.INCOME:
                self._total_income += transaction.amount
                self._balance += transaction.amount
            else:
                self._total_expense += transaction.amount
                self._balance -= transaction.amount

    def add_income(self, 
                amount: Decimal,
                category: Category, 
                description:str = "",
                tags: tuple[str, ...] = None
                ) -> Transaction:
        transaction = self.factory.create_income(amount, category, description,tags)
        saved_transaction = self.repository.add(transaction)
        self._balance += amount
        self._total_income += amount
        return saved_transaction

        
    def add_expense(self, 
                amount: Decimal,
                category: Category, 
                description:str = "", 
                tags: Optional[tuple[str, ...]] = None
                ) -> Transaction:
        transaction = self.factory.create_expense(amount, category, description,tags)
        saved_transaction = self.repository.add(transaction)
        self._balance -= amount
        self._total_expense += amount
        return saved_transaction

    def get_balance(self) -> Decimal:
        return self._balance

    def get_total_income(self):
        return self._total_income
    
    def get_total_expense(self)-> Decimal:
        return self._total_expense
    
    def get_report(self,report_generator: ReportGenerator) -> str:
        transactions = self.repository.get_all()
        return report_generator.generate(transactions)