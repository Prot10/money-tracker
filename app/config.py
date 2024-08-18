"""Module to store configuration variables."""

from pathlib import Path

API_KEY_FILE = "app/key.txt"

with open(API_KEY_FILE, "r") as file:
    API_KEY = file.read().strip()
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
CSV_PATH = Path("app/data") / "expenses.csv"
DATE_FORMAT = "%d-%m-%Y"

dark_mode_colors = {
    "title": "#FFD700",  # Gold
    "background": "#202123",  # Dark background
    "text": "#D1D5DB",  # Light gray text
    "block": "#3E4149",  # Block background
    "input_block": "#2D2F34",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#3E4149",  # Table background
    "subtitle": "#FFFFFF",  # White
}

light_mode_colors = {
    "title": "#FFD700",  # Gold
    "background": "#FFFFFF",  # Light background
    "text": "#202123",  # Dark text
    "block": "#F0F0F0",  # Light block background
    "input_block": "#E0E0E0",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#FFFFFF",  # Table background
    "subtitle": "#000000",  # Black
}

color_palette = [
    "#10B981",  # Emerald green
    "#EF4444",  # Red
    "#3B82F6",  # Blue
    "#F59E0B",  # Amber
    "#8B5CF6",  # Violet
    "#EC4899",  # Pink
    "#F97316",  # Orange
    "#22D3EE",  # Cyan
    "#4B5563",  # Cool gray
    "#14B8A6",  # Teal
    "#A855F7",  # Purple
    "#EAB308",  # Yellow
]
