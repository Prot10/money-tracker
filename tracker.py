"""Main module for the expense tracker."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from pydantic import BaseModel, validator

CSV_PATH = Path("data") / "expenses.csv"

DATE_FORMAT = "%d-%m-%Y"


class Expense(BaseModel):
    category: str
    cost: float
    note: str
    date: str
    currency: str
    account: str

    @validator("date")
    def validate_date(cls, v):
        """Validate and ensure the date is in the correct format."""
        try:
            datetime.strptime(v, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Date must be in the format {DATE_FORMAT}")
        return v


class ExpenseTracker:
    def __init__(self, csv_file: Path = CSV_PATH):
        self.csv_file = Path(csv_file)
        self.expenses: List[Expense] = []
        self._load_expenses()

    def _load_expenses(self):
        """Load existing expenses from the CSV file."""
        if self.csv_file.exists():
            with self.csv_file.open(mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense(
                        category=row["category"],
                        cost=float(row["cost"]),
                        note=row["note"],
                        date=row["date"],  # Already in dd-mm-yyyy format
                        currency=row["currency"],
                        account=row["account"],
                    )
                    self.expenses.append(expense)

    def add_expense(
        self,
        category: str,
        cost: float,
        note: str,
        date: str,
        currency: str,
        account: str,
    ):
        """Add a new expense."""
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Date must be in the format {DATE_FORMAT}")

        expense = Expense(
            category=category,
            cost=cost,
            note=note,
            date=date,
            currency=currency,
            account=account,
        )
        self.expenses.append(expense)
        self._save_expense_to_csv(expense)

    def _save_expense_to_csv(self, expense: Expense):
        """Save a single expense to the CSV file."""
        file_exists = self.csv_file.is_file()
        with self.csv_file.open(mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=Expense.__fields__.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(expense.dict())

    def get_expenses(self) -> List[Expense]:
        """Return the list of expenses."""
        return self.expenses

    def get_summary_by_category(self):
        """Generate a summary of expenses by category."""
        summary = {}
        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = 0
            summary[expense.category] += expense.cost
        return summary


# Example usage:
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.add_expense("Food", 15.99, "Lunch", "17-08-2024", "USD", "Credit Card")
    tracker.add_expense("Transport", 2.50, "Bus fare", "17-08-2024", "USD", "Cash")
    print(tracker.get_expenses())
    print(tracker.get_summary_by_category())
