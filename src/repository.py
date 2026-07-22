from abc import ABC,abstractmethod
from datetime import datetime
from typing import List

from models import Category, Transaction

class TransactionsRepository(ABC):
    @abstractmethod
    def add(self,transaction:Transaction):
        pass
    
    @abstractmethod
    def get_all(self) -> List(Transaction):
        pass
    @abstractmethod
    def get_by_category(self, category_name:str) -> List(Transaction):
        pass

    @abstractmethod
    def get_by_date(self, start:datetime, end:datetime) -> List(Transaction):
        pass


class InMemoryTransactionRepository(TransactionsRepository):
    
    def __init__(self):
        self._transactions: List(Transaction) = [] 
        self._id = 1
    
    def add(self, transaction: Transaction):
        # self.transaction.id = self._id  # pay ATTENTION !!!
        # bacause of frozen true we cann't only modify the id.
        # a whole new object is created, check for better solutions.
        # Check ?
        transaction_with_id = Transaction(
            id=self._next_id,
            amount=transaction.amount,
            type=transaction.type,
            category=transaction.category,
            date=transaction.date,
            description=transaction.description,
            tags=transaction.tags
        )
        self._transactions.append(transaction_with_id)
        self._id += 1
    
    def get_all(self) -> List[Transaction]: 
        return self._transactions.copy()
    
    def get_by_category(self, category_name: str) -> List[Transaction]:
        return [t for t in self._transactions if t.category.name == category_name]
    
    def get_by_date(self, start: datetime, end: datetime ) -> List[Transaction]:
        return [t for t in self._transactions if start <= t.date <= end ]