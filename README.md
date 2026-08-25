# Expense Tracker

A clean, well-structured personal expense tracker built in Python to demonstrate solid Object-Oriented Programming and **SOLID principles**.

## Features

- Add income and expenses
- Categorize transactions
- Running balance (efficient, real-world style)
- Generate reports
- Immutable data models
- Extensible design (easy to add new storage or report types)

## SOLID Principles Applied

|                               | Principle                                                                                                                                                                               | How it is applied in this project |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| **S** - Single Responsibility | Each class has one clear responsibility: `Transaction` holds data, `ExpenseTracker` manages business logic, `ReportGenerator` creates reports, `TransactionRepository` handles storage. |
| **O** - Open/Closed           | You can add new report types or new storage backends (JSON, SQLite, etc.) without modifying existing code.                                                                              |
| **L** - Liskov Substitution   | Any class that implements `TransactionRepository` can be used interchangeably with `InMemoryTransactionRepository`.                                                                     |
| **I** - Interface Segregation | Small and focused interfaces (`TransactionRepository` and `ReportGenerator`) instead of one large interface.                                                                            |
| **D** - Dependency Inversion  | High-level modules (`ExpenseTracker`) depend on abstractions, not concrete implementations.                                                                                             |                                   |

## Project Structure

expense-tracker/
│
├── src/
│ └── expense_tracker/
│ ├── **init**.py
│ ├── models.py # Immutable data classes
│ ├── repository.py # Storage abstraction + InMemory implementation
│ ├── factory.py # Clean object creation
│ ├── report.py # Report generation (extensible)
│ └── tracker.py # Main business logic (Running Balance)
│
├── tests/
│
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── .gitignore

git@github.com:Mahya-Asg/expense-tracker.git
https://github.com/Mahya-Asg/expense-tracker.git
