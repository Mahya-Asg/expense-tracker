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

| Principle | How it is applied |
|---------|-------------------|
| **S** - Single Responsibility | Each class has one clear job (`Transaction`, `ExpenseTracker`, `ReportGenerator`, etc.) |
| **O** - Open/Closed | Easy to add new report formats or storage backends without changing existing code |
| **L** - Liskov Substitution | Any class implementing `TransactionRepository` can be used interchangeably |
| **I** - Interface Segregation | Small, focused abstract interfaces (`TransactionRepository`, `ReportGenerator`) |
| **D** - Dependency Inversion | High-level modules depend on abstractions, not concrete implementations |

## Project Structure

src/
├── models.py          # Immutable data classes
├── repository.py      # Storage abstraction + InMemory implementation
├── factory.py         # Clean object creation
├── report.py          # Report generation (extensible)
└── tracker.py         # Main business logic (Running Balance)

expense-tracker/
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   ├── factory.py
│   ├── report.py
│   └── tracker.py
├── main.py
├── README.md
├── requirements.txt
└── .gitignore


expense-tracker/
│
├── src/
│   └── expense_tracker/
│       ├── __init__.py
│       ├── models.py
│       ├── repository.py
│       ├── factory.py
│       ├── report.py
│       └── tracker.py
│
├── tests/
│
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── .gitignore


