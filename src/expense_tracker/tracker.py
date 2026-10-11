import logging
from decimal import Decimal

from .factory import TransactionFactory
from .models import Category, Transaction, TransactionType
from .report import ReportGenerator
from .repository import TransactionsRepository

logger = logging.getLogger(__name__)


class ExpenseTracker:
    def __init__(self, repository: TransactionsRepository, factory:TransactionFactory | None=None):
        self.repository = repository
        self.factory = factory or TransactionFactory()

       # Initialize and calculate totals from existing data
        self._recalculate_totals()
        logger.info("ExpenseTracker initialized.")

    def _recalculate_totals(self):
        """
        Recalculate running balance, total income and total expense
        based on all transactions currently in the repository.
        """
        self._balance: Decimal = Decimal(0)
        self._total_income: Decimal = Decimal(0)
        self._total_expense: Decimal = Decimal(0)
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
                tags: tuple[str, ...] | None = None
                ) -> Transaction:
        transaction = self.factory.create_income(amount, category, description,tags)
        # use the saved_transaction for the updated id in the repository.add
        saved_transaction = self.repository.add(transaction)
        self._balance += amount
        self._total_income += amount
        logger.info(f"Income added: {amount} | {category.name}")
        return saved_transaction

        
    def add_expense(self, 
                amount: Decimal,
                category: Category, 
                description:str = "", 
                tags: tuple[str, ...] | None = None
                ) -> Transaction:
        transaction = self.factory.create_expense(amount, category, description,tags)
        # use the saved_transaction for the updated id in the repository.add
        saved_transaction = self.repository.add(transaction)
        self._balance -= amount
        self._total_expense += amount
        logger.info(f"Expense added: {amount} | {category.name}")
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