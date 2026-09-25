import logging
from decimal import Decimal


from expense_tracker.logger_config import setup_logger
from  expense_tracker.models import Category
from  expense_tracker.repository import InMemoryTransactionRepository
from  expense_tracker.tracker import ExpenseTracker
from  expense_tracker.report import ConsoleReportGenerator
# using JSON
from expense_tracker.json_repository import JSONTransactionRepository

# Configure logging only once
logger = setup_logger()

def main():
    logger.info("Starting Expense Tracker...")

    repo = JSONTransactionRepository("data/transactions.jsonl")
    tracker = ExpenseTracker(repo)
    report_gen = ConsoleReportGenerator()

    # Sample data
    logger.info("Adding sample transactions.")
    salary = Category("Salary")
    food = Category("Food")
    rent = Category("Rent")

    tracker.add_income(Decimal("6000"), salary, "July Salary")
    tracker.add_expense(Decimal("1500"), rent, "Monthly Rent")
    tracker.add_expense(Decimal("300"), food, "Groceries")

    print(tracker.get_report(report_gen))
    print(f"Quick Balance Check: {tracker.get_balance()}")
    
    logger.info("Expense Tracker finished.")

if __name__ == "__main__":
    main()