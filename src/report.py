from abc import ABC, abstractmethod

from models import Transaction, TransactionType
# from repository import TransactionsRepository, InMemoryTransactionRepository


class TransactionReport(ABC):
    @abstractmethod
    def generate(self, transactions: List[Transaction]) -> str:
        pass


class ConsoleTransactionReport(TransactionReport):
    def generate(self, transactions: List[Transaction]) -> str:
        if not transactions:
            return "No transactions found."

        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        balance = total_income - total_expense
    
        report = "\n=== EXPENSE REPORT ===\n"   
        report += f"Total Transactions: {len(transactions)}\n"
        report += f"Total Income      : {total_income}\n"
        report += f"Total Expense     : {total_expense}\n"
        report += f"Current Balance   : {total_expense}\n\n"
        report += "Transactions:\n"
        
        for t in sorted(transactions, key=lambda x: x.date, reverse=True):
            sign = "+" if t.type == TransactionType.INCOME else "-"
            report += f"{t.date.strftime('%Y-%m-%d %H:%M')} | {sign}{t.amount:8} | {t.category.name:12} | {t.description}\n" 

        return report
