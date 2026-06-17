"""Data storage for the budget tracker."""

import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "expenses.json"


def load_expenses():
    """Load stored expenses from a JSON file."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_expenses(expenses):
    """Save the expense list to a JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(expenses, handle, indent=2)


def create_expense(amount, category, description):
    """Create a new expense record."""
    return {
        "date": date.today().isoformat(),
        "amount": amount,
        "category": category,
        "description": description,
    }
