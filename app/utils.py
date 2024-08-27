"""Module containing utility functions for the expenses tracker app."""

import logging

import pandas as pd
import requests

from .config import BASE_URL, CSV_PATH
from .data.tracker import ExpenseTracker

DEFAULT_RATES = {"EUR": 1.0, "USD": 0.8958, "GBP": 0.8465, "CHF": 0.9460}


def get_exchange_rate(from_currency: str, to_currency: str = "EUR") -> float:
    """Fetch the exchange rate from one currency to another, using default rates if necessary."""
    try:
        url = f"{BASE_URL}{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "conversion_rates" not in data:
            logging.error(
                f"Failed to fetch exchange rate: {data.get('error-type', 'Unknown error')}"
            )
            return DEFAULT_RATES.get(
                to_currency, 1.0
            )  # Return default rate if API fails

        rate = data["conversion_rates"].get(to_currency)
        if rate is None:
            logging.error(f"Conversion rate for {to_currency} not found in response.")
            return DEFAULT_RATES.get(
                to_currency, 1.0
            )  # Return default rate if conversion rate not found

        return rate
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {str(e)}")
        return DEFAULT_RATES.get(to_currency, 1.0)  # Return default rate on exception


def convert_to_euro(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the cost column to EUR using the exchange rates."""

    def safe_convert(row: pd.Series) -> float | None:
        """Safely convert the cost to EUR."""
        try:
            if row["currency"] == "EUR":
                return row["cost"]
            else:
                rate = get_exchange_rate(row["currency"], "EUR")
                if rate is not None:
                    return row["cost"] * rate
                else:
                    return None
        except Exception as e:
            logging.error(f"Failed to convert {row['currency']} to EUR: {str(e)}")
            return None

    df["cost_euro"] = df.apply(safe_convert, axis=1)
    # Handle any rows where conversion failed by dropping or filling with 0
    df = df.dropna(subset=["cost_euro"])
    return df


def ensure_csv_exists():
    """Ensure the CSV file exists, creating it if necessary."""
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        ).to_csv(CSV_PATH, index=False)


def load_expenses(expense_tracker: ExpenseTracker) -> pd.DataFrame:
    """Load expenses from the CSV file."""
    df = pd.DataFrame([expense.dict() for expense in expense_tracker.get_expenses()])
    if df.empty:
        df = pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        )
    return df


def convert_income_to_euro(amount: float, currency: str) -> float:
    """Convert the given amount from the specified currency to euros.

    Args:
        amount (float): The amount of money to convert.
        currency (str): The currency of the amount (e.g., 'EUR', 'USD', 'GBP', 'CHF').

    Returns:
        float: The equivalent amount in euros.
    """
    if currency == "EUR":
        return amount
    rate = get_exchange_rate(currency, "EUR")
    if rate is not None:
        return amount * rate
    return None
