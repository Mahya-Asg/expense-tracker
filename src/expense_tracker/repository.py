from abc import ABC,abstractmethod
from datetime import datetime

from .models import Category, Transaction

class TransactionsRepository(ABC):
    @abstractmethod
    def add(self,transaction:Transaction):
        pass
    
    @abstractmethod
    def get_all(self) -> list[Transaction]:
        pass
    @abstractmethod
    def get_by_category(self, category_name:str) -> list[Transaction]:
        pass

    @abstractmethod
    def get_by_date(self, start:datetime, end:datetime) -> list[Transaction]:
        pass


class InMemoryTransactionRepository(TransactionsRepository):
    
    def __init__(self):
        self._transactions: list[Transaction] = [] 
        self._id = 1
    
    def add(self, transaction: Transaction):
        # self.transaction.id = self._id  # pay ATTENTION !!!
        # bacause of frozen true we cann't only modify the id.
        # a whole new object is created, check for better solutions.
        # Check ?
        transaction_with_id = Transaction(
            id=self._id,
            amount=transaction.amount,
            type=transaction.type,
            category=transaction.category,
            date=transaction.date,
            description=transaction.description,
            tags=transaction.tags
        )
        self._transactions.append(transaction_with_id)
        self._id += 1
        return transaction_with_id
    
    def get_all(self) -> list[Transaction]: 
        return self._transactions.copy()
    
    def get_by_category(self, category_name: str) -> list[Transaction]:
        return [t for t in self._transactions if t.category.name == category_name]
    
    def get_by_date(self, start: datetime, end: datetime ) -> list[Transaction]:
        return [t for t in self._transactions if start <= t.date <= end ]