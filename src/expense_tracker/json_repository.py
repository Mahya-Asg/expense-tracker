# version 4
import json
from decimal import Decimal
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import List

from expense_tracker.models import Category, Transaction, TransactionType
from expense_tracker.repository import TransactionsRepository

logger = logging.getLogger(__name__)

class JSONTransactionRepository(TransactionsRepository):
    """
    JSON Lines (JSONL) based persistence.
    Each transaction is one JSON object per line.
    This is more efficient for append operations.
    """

    def __init__(self, file_path: str = "data/transactions.jsonl") -> None:
        self.file_path = Path(file_path)
        self._transactions: List[Transaction] = []
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load all transactions from JSON Lines file."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            return

        try:
            self._transactions = []
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    item = json.loads(line)
                    transaction = Transaction(
                        id=item["id"],
                        amount=Decimal(item["amount"]),
                        type=TransactionType(item["type"]),
                        category=Category(item["category"]),
                        date=datetime.fromisoformat(item["date"]),
                        description=item.get("description", ""),
                        tags=tuple(item["tags"]) if item.get("tags") else None,
                    )
                    self._transactions.append(transaction)


            self._next_id = max((t.id for t in self._transactions), default=1) + 1
        except Exception as e:
            print(f"Warning: Could not load transactions. Starting fresh.\nError: {e}")
            self._transactions = []
            self._next_id = 1

    def _save(self, transaction: Transaction) -> None:
        """Save one transaction to the JSONL file (append-only)."""
        data = {
            "id": transaction.id,
            "amount": str(transaction.amount),
            "type": transaction.type.value,
            "category": transaction.category.name,
            "date": transaction.date.isoformat(),
            "description": transaction.description,
            "tags": list(transaction.tags) if transaction.tags else None,
        }

        # Ensure the directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            file.write("\n")

    def add(self, transaction: Transaction) -> None:
        """Add transaction and append to JSON Lines file."""
        transaction_with_id = replace(transaction, id=self._next_id)  # from dataclasses import replace
        self._transactions.append(transaction_with_id)
        self._next_id += 1
        self._save(transaction_with_id)

    def get_all(self) -> List[Transaction]:
        return self._transactions.copy()

    def get_by_category(self, category_name: str) -> List[Transaction]:
        return [t for t in self._transactions if t.category.name == category_name]

    def get_by_date(self, start: datetime, end: datetime) -> List[Transaction]:
        return [t for t in self._transactions if start <= t.date <= end]


