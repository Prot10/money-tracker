import logging
from datetime import datetime

import dash
import pandas as pd
import requests
from dash import Input, Output, State, dash_table, dcc, html

from tracker import CSV_PATH, ExpenseTracker

API_KEY = "..."
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"


# Function to get the exchange rate from ExchangeRate-API
def get_exchange_rate(from_currency, to_currency="EUR"):
    try:
        url = f"{BASE_URL}{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "conversion_rates" not in data:
            logging.error(
                f"Failed to fetch exchange rate: {data.get('error-type', 'Unknown error')}"
            )
            return None

        rate = data["conversion_rates"].get(to_currency)
        if rate is None:
            logging.error(f"Conversion rate for {to_currency} not found in response.")
            return None
        return rate
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {str(e)}")
        return None


# Function to convert costs to Euro with error handling
def convert_to_euro(df):
    def safe_convert(row):
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


# Ensure the CSV file exists
def ensure_csv_exists():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        ).to_csv(CSV_PATH, index=False)


ensure_csv_exists()

# Initialize the ExpenseTracker
expense_tracker = ExpenseTracker()

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap"
    ],
)


# Load existing data
def load_expenses():
    df = pd.DataFrame([expense.dict() for expense in expense_tracker.get_expenses()])
    if df.empty:
        df = pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        )
    return df


# # Define the color palette
# colors = {
#     "background": "#3F334D",  # Background color
#     "text": "#FFFFFF",  # White text
#     "block": "#7D8491",  # Block background
#     "input_block": "#7D8491",  # Input commands block
#     "button": "#574B60",  # Button and table header
#     "table_bg": "#C0C5C1",  # Table background
# }

# # Create a palette excluding the block background color
# color_palette = [
#     colors["text"],  # White text
#     colors["button"],  # Button color
#     colors["table_bg"],  # Table background
# ]

# # Add additional colors to match the style
# additional_colors = [
#     "#FF6F61",  # Coral
#     "#6B5B95",  # Purple
#     "#88B04B",  # Green
#     "#F7CAC9",  # Pink
#     "#92A8D1",  # Blue
# ]

# # Combine the existing and additional colors
# color_palette.extend(additional_colors)

# Define the color palette
# colors = {
#     "background": "#202123",  # Dark background
#     "text": "#D1D5DB",  # Light gray text
#     "block": "#3E4149",  # Block background
#     "input_block": "#2D2F34",  # Input commands block
#     "button": "#6366F1",  # Button and table header
#     "table_bg": "#3E4149",  # Table background
#     "white": "#FFFFFF",  # White
# }

dark_mode_colors = {
    "background": "#202123",  # Dark background
    "text": "#D1D5DB",  # Light gray text
    "block": "#3E4149",  # Block background
    "input_block": "#2D2F34",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#3E4149",  # Table background
    "subtitle": "#FFFFFF",  # White
}

light_mode_colors = {
    "background": "#FFFFFF",  # Light background
    "text": "#202123",  # Dark text
    "block": "#F0F0F0",  # Light block background
    "input_block": "#E0E0E0",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#FFFFFF",  # Table background,
    "subtitle": "#000000",  # Black
}


# Add additional colors for plotting
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
# Define the color palettes
dark_mode_colors = {
    "title": "#FFD700",
    "background": "#202123",  # Dark background
    "text": "#D1D5DB",  # Light gray text
    "block": "#3E4149",  # Block background
    "input_block": "#2D2F34",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#3E4149",  # Table background
    "subtitle": "#FFFFFF",  # White
}

light_mode_colors = {
    "title": "#FFD700",
    "background": "#FFFFFF",  # Light background
    "text": "#202123",  # Dark text
    "block": "#F0F0F0",  # Light block background
    "input_block": "#E0E0E0",  # Input commands block
    "button": "#6366F1",  # Button and table header
    "table_bg": "#FFFFFF",  # Table background
    "subtitle": "#000000",  # Black
}

# Use light mode by default
colors = dark_mode_colors


# Function to get the exchange rate from ExchangeRate-API
def get_exchange_rate(from_currency, to_currency="EUR"):
    try:
        url = f"{BASE_URL}{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "conversion_rates" not in data:
            logging.error(
                f"Failed to fetch exchange rate: {data.get('error-type', 'Unknown error')}"
            )
            return None

        rate = data["conversion_rates"].get(to_currency)
        if rate is None:
            logging.error(f"Conversion rate for {to_currency} not found in response.")
            return None
        return rate
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {str(e)}")
        return None


# Function to convert costs to Euro with error handling
def convert_to_euro(df):
    def safe_convert(row):
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


# Ensure the CSV file exists
def ensure_csv_exists():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        ).to_csv(CSV_PATH, index=False)


ensure_csv_exists()

# Initialize the ExpenseTracker
expense_tracker = ExpenseTracker()

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap"
    ],
)

# Layout of the app
app.layout = html.Div(
    id="main-container",
    style={
        "backgroundColor": colors["background"],
        "fontFamily": "'Indie Flower', cursive",
        "margin": "0",
        "padding": "0",
        "minHeight": "100vh",
        "position": "relative",
    },
    children=[
        html.Button(
            "Toggle Light/Dark Mode",
            id="toggle-button",
            style={
                "position": "absolute",
                "top": "10px",
                "right": "10px",
                "backgroundColor": colors["button"],
                "color": colors["subtitle"],
                "borderRadius": "5px",
                "padding": "10px",
                "fontSize": "15px",
            },
        ),
        html.H1(
            "The Expense Tracker",
            style={
                "textAlign": "center",
                "color": colors["title"],
                "padding": "20px",
                "fontSize": "60px",
                "marginBottom": "5px",
                "marginTop": "5px",
            },
        ),
        html.Div(
            id="app-content",
            children=[
                html.Div(
                    [
                        html.Div(
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "1fr 1fr",
                                "gap": "10px",
                            },
                            children=[
                                html.Div(
                                    children=[
                                        html.H3(
                                            "Add New Expense",
                                            style={
                                                "color": colors["subtitle"],
                                                "textAlign": "center",
                                                "fontSize": "30px",
                                                "marginBottom": "5px",
                                                "marginTop": "5px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Category",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="input-category",
                                                    type="text",
                                                    value="",
                                                    placeholder="e.g., Food",
                                                    style={
                                                        "width": "40%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Cost",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="input-cost",
                                                    type="number",
                                                    value=None,
                                                    placeholder="e.g., 20.5",
                                                    style={
                                                        "width": "40%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Note",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="input-note",
                                                    type="text",
                                                    value="",
                                                    placeholder="e.g., Lunch with friends (Optional)",
                                                    style={
                                                        "width": "60%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Date",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.DatePickerSingle(
                                                    id="input-date",
                                                    date=datetime.now().strftime(
                                                        "%Y-%m-%d"
                                                    ),
                                                    display_format="DD-MM-YYYY",
                                                    style={
                                                        "width": "40%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Currency",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Dropdown(
                                                    id="input-currency",
                                                    options=[
                                                        {
                                                            "label": "Euro (€)",
                                                            "value": "EUR",
                                                        },
                                                        {
                                                            "label": "US Dollar ($)",
                                                            "value": "USD",
                                                        },
                                                        {
                                                            "label": "British Pound (£)",
                                                            "value": "GBP",
                                                        },
                                                        {
                                                            "label": "Swiss Franc (CHF)",
                                                            "value": "CHF",
                                                        },
                                                    ],
                                                    value="EUR",
                                                    style={
                                                        "width": "50%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                    clearable=False,
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Account",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="input-account",
                                                    type="text",
                                                    value="",
                                                    placeholder="e.g., Credit Card",
                                                    style={
                                                        "width": "40%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Button(
                                            "Add Expense",
                                            id="add-expense-button",
                                            n_clicks=0,
                                            style={
                                                "width": "40%",
                                                "margin": "10px auto",
                                                "backgroundColor": colors["button"],
                                                "color": colors["text"],
                                                "borderRadius": "5px",
                                                "display": "block",
                                                "fontSize": "15px",
                                            },
                                        ),
                                        html.Div(
                                            id="error-message",
                                            style={
                                                "color": colors["button"],
                                                "marginTop": "10px",
                                                "textAlign": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "gridColumn": "1 / 2",
                                        "backgroundColor": colors["block"],
                                        "padding": "20px",
                                        "borderRadius": "8px",
                                        "marginBottom": "20px",
                                        "marginRight": "20px",
                                    },
                                ),
                                html.Div(
                                    children=[
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Income setup",
                                                    style={
                                                        "color": colors["subtitle"],
                                                        "textAlign": "center",
                                                        "fontSize": "30px",
                                                        "marginBottom": "5px",
                                                        "marginTop": "5px",
                                                    },
                                                ),
                                                html.Label(
                                                    "Monthly Income",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="input-monthly-income",
                                                    type="number",
                                                    value=None,
                                                    placeholder="Set monthly income",
                                                    style={
                                                        "width": "40%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                ),
                                                html.Label(
                                                    "Currency",
                                                    style={
                                                        "color": colors["text"],
                                                        "display": "block",
                                                        "textAlign": "center",
                                                        "fontStyle": "italic",
                                                        "fontSize": "20px",
                                                    },
                                                ),
                                                dcc.Dropdown(
                                                    id="input-income-currency",
                                                    options=[
                                                        {
                                                            "label": "Euro (€)",
                                                            "value": "EUR",
                                                        },
                                                        {
                                                            "label": "US Dollar ($)",
                                                            "value": "USD",
                                                        },
                                                        {
                                                            "label": "British Pound (£)",
                                                            "value": "GBP",
                                                        },
                                                        {
                                                            "label": "Swiss Franc (CHF)",
                                                            "value": "CHF",
                                                        },
                                                    ],
                                                    value="EUR",
                                                    style={
                                                        "width": "50%",
                                                        "margin": "0 auto 10px auto",
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                    },
                                                    clearable=False,
                                                ),
                                                html.Button(
                                                    "Update Income",
                                                    id="set-income-button",
                                                    n_clicks=0,
                                                    style={
                                                        "width": "40%",
                                                        "margin": "10px auto",
                                                        "backgroundColor": colors[
                                                            "button"
                                                        ],
                                                        "color": colors["text"],
                                                        "borderRadius": "5px",
                                                        "display": "block",
                                                        "fontSize": "15px",
                                                    },
                                                ),
                                                html.Div(
                                                    id="income-update-message",
                                                    style={
                                                        "color": colors["text"],
                                                        "textAlign": "center",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "marginBottom": "20px",
                                                "backgroundColor": colors["block"],
                                                "padding": "20px",
                                                "borderRadius": "8px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Statistics",
                                                    style={
                                                        "color": colors["subtitle"],
                                                        "textAlign": "center",
                                                        "fontSize": "30px",
                                                        "marginBottom": "5px",
                                                        "marginTop": "5px",
                                                    },
                                                ),
                                                html.Div(id="statistics-output"),
                                            ],
                                            style={
                                                "marginBottom": "20px",
                                                "backgroundColor": colors["block"],
                                                "padding": "20px",
                                                "borderRadius": "8px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "gridColumn": "2 / 3",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.H3(
                                    "Expenses",
                                    style={
                                        "color": colors["subtitle"],
                                        "textAlign": "center",
                                        "fontSize": "30px",
                                        "marginBottom": "5px",
                                        "marginTop": "5px",
                                    },
                                ),
                                dash_table.DataTable(
                                    id="expenses-table",
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in [
                                            "category",
                                            "cost",
                                            "note",
                                            "date",
                                            "currency",
                                            "account",
                                            "cost_euro",
                                        ]
                                    ],
                                    data=load_expenses().to_dict("records"),
                                    style_table={
                                        "overflowX": "auto",
                                        "borderRadius": "8px",
                                    },
                                    style_header={
                                        "backgroundColor": colors["button"],
                                        "color": colors["text"],
                                        "fontWeight": "bold",
                                    },
                                    style_cell={
                                        "backgroundColor": colors["table_bg"],
                                        "color": colors["text"],
                                        "textAlign": "center",
                                        "padding": "10px",
                                    },
                                    style_filter={
                                        "backgroundColor": colors["text"],
                                        "color": colors["text"],
                                        "border": "1px solid " + colors["button"],
                                    },
                                    style_as_list_view=True,
                                    page_size=10,  # Limit to 10 rows
                                    sort_action="native",
                                    filter_action="native",
                                ),
                            ],
                            style={
                                "backgroundColor": colors["block"],
                                "padding": "20px",
                                "borderRadius": "8px",
                            },
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "20px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Expenses by Category",
                                    style={
                                        "color": colors["subtitle"],
                                        "textAlign": "center",
                                        "fontSize": "30px",
                                        "marginBottom": "5px",
                                        "marginTop": "5px",
                                    },
                                ),
                                dcc.Graph(
                                    id="category-summary",
                                    style={"height": "440px", "borderRadius": "8px"},
                                ),
                            ],
                            style={
                                "backgroundColor": colors["block"],
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.H3(
                                    "Monthly Expenses by Category",
                                    style={
                                        "color": colors["subtitle"],
                                        "textAlign": "center",
                                        "fontSize": "30px",
                                        "marginBottom": "5px",
                                        "marginTop": "5px",
                                    },
                                ),
                                dcc.Graph(
                                    id="monthly-summary",
                                    style={"height": "478px", "borderRadius": "8px"},
                                ),
                            ],
                            style={
                                "backgroundColor": colors["block"],
                                "padding": "20px",
                                "borderRadius": "8px",
                            },
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "20px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
            },
        ),
    ],
)


# Callback to toggle between light and dark mode
@app.callback(
    Output("main-container", "style"),
    Output("toggle-button", "style"),
    Output("app-content", "children"),
    Input("toggle-button", "n_clicks"),
)
def toggle_light_dark_mode(n_clicks):
    global colors  # Ensure we are using the global 'colors' variable

    if n_clicks is None or n_clicks % 2 == 0:
        colors = light_mode_colors
    else:
        colors = dark_mode_colors

    container_style = {
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "fontFamily": "'Indie Flower', cursive",
        "minHeight": "100vh",
        "position": "relative",
    }

    button_style = {
        "position": "absolute",
        "top": "10px",
        "right": "10px",
        "backgroundColor": colors["button"],
        "color": colors["subtitle"],
        "borderRadius": "5px",
        "padding": "10px",
        "fontSize": "15px",
    }

    app_content = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "10px",
                        },
                        children=[
                            html.Div(
                                children=[
                                    html.H3(
                                        "Add New Expense",
                                        style={
                                            "color": colors["subtitle"],
                                            "textAlign": "center",
                                            "fontSize": "30px",
                                            "marginBottom": "5px",
                                            "marginTop": "5px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Category",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Input(
                                                id="input-category",
                                                type="text",
                                                value="",
                                                placeholder="e.g., Food",
                                                style={
                                                    "width": "40%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Cost",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Input(
                                                id="input-cost",
                                                type="number",
                                                value=None,
                                                placeholder="e.g., 20.5",
                                                style={
                                                    "width": "40%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Note",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Input(
                                                id="input-note",
                                                type="text",
                                                value="",
                                                placeholder="e.g., Lunch with friends (Optional)",
                                                style={
                                                    "width": "60%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Date",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.DatePickerSingle(
                                                id="input-date",
                                                date=datetime.now().strftime(
                                                    "%Y-%m-%d"
                                                ),
                                                display_format="DD-MM-YYYY",
                                                style={
                                                    "width": "40%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Currency",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Dropdown(
                                                id="input-currency",
                                                options=[
                                                    {
                                                        "label": "Euro (€)",
                                                        "value": "EUR",
                                                    },
                                                    {
                                                        "label": "US Dollar ($)",
                                                        "value": "USD",
                                                    },
                                                    {
                                                        "label": "British Pound (£)",
                                                        "value": "GBP",
                                                    },
                                                    {
                                                        "label": "Swiss Franc (CHF)",
                                                        "value": "CHF",
                                                    },
                                                ],
                                                value="EUR",
                                                style={
                                                    "width": "50%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                                clearable=False,
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Account",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Input(
                                                id="input-account",
                                                type="text",
                                                value="",
                                                placeholder="e.g., Credit Card",
                                                style={
                                                    "width": "40%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                        ]
                                    ),
                                    html.Button(
                                        "Add Expense",
                                        id="add-expense-button",
                                        n_clicks=0,
                                        style={
                                            "width": "40%",
                                            "margin": "10px auto",
                                            "backgroundColor": colors["button"],
                                            "color": colors["subtitle"],
                                            "borderRadius": "5px",
                                            "display": "block",
                                            "fontSize": "15px",
                                        },
                                    ),
                                    html.Div(
                                        id="error-message",
                                        style={
                                            "color": colors["button"],
                                            "marginTop": "10px",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "gridColumn": "1 / 2",
                                    "backgroundColor": colors["block"],
                                    "padding": "20px",
                                    "borderRadius": "8px",
                                    "marginBottom": "20px",
                                    "marginRight": "20px",
                                },
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        [
                                            html.H3(
                                                "Income setup",
                                                style={
                                                    "color": colors["subtitle"],
                                                    "textAlign": "center",
                                                    "fontSize": "30px",
                                                    "marginBottom": "5px",
                                                    "marginTop": "5px",
                                                },
                                            ),
                                            html.Label(
                                                "Monthly Income",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Input(
                                                id="input-monthly-income",
                                                type="number",
                                                value=None,
                                                placeholder="Set monthly income",
                                                style={
                                                    "width": "40%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                            ),
                                            html.Label(
                                                "Currency",
                                                style={
                                                    "color": colors["text"],
                                                    "display": "block",
                                                    "textAlign": "center",
                                                    "fontStyle": "italic",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            dcc.Dropdown(
                                                id="input-income-currency",
                                                options=[
                                                    {
                                                        "label": "Euro (€)",
                                                        "value": "EUR",
                                                    },
                                                    {
                                                        "label": "US Dollar ($)",
                                                        "value": "USD",
                                                    },
                                                    {
                                                        "label": "British Pound (£)",
                                                        "value": "GBP",
                                                    },
                                                    {
                                                        "label": "Swiss Franc (CHF)",
                                                        "value": "CHF",
                                                    },
                                                ],
                                                value="EUR",
                                                style={
                                                    "width": "50%",
                                                    "margin": "0 auto 10px auto",
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                },
                                                clearable=False,
                                            ),
                                            html.Button(
                                                "Update Income",
                                                id="set-income-button",
                                                n_clicks=0,
                                                style={
                                                    "width": "40%",
                                                    "margin": "10px auto",
                                                    "backgroundColor": colors["button"],
                                                    "color": colors["text"],
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                    "fontSize": "15px",
                                                },
                                            ),
                                            html.Div(
                                                id="income-update-message",
                                                style={
                                                    "color": colors["text"],
                                                    "textAlign": "center",
                                                },
                                            ),
                                        ],
                                        style={
                                            "marginBottom": "20px",
                                            "backgroundColor": colors["block"],
                                            "padding": "20px",
                                            "borderRadius": "8px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.H3(
                                                "Statistics",
                                                style={
                                                    "color": colors["subtitle"],
                                                    "textAlign": "center",
                                                    "fontSize": "30px",
                                                    "marginBottom": "5px",
                                                    "marginTop": "5px",
                                                },
                                            ),
                                            html.Div(id="statistics-output"),
                                        ],
                                        style={
                                            "marginBottom": "20px",
                                            "backgroundColor": colors["block"],
                                            "padding": "20px",
                                            "borderRadius": "8px",
                                        },
                                    ),
                                ],
                                style={
                                    "gridColumn": "2 / 3",
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Expenses",
                                style={
                                    "color": colors["subtitle"],
                                    "textAlign": "center",
                                    "fontSize": "30px",
                                    "marginBottom": "5px",
                                    "marginTop": "5px",
                                },
                            ),
                            dash_table.DataTable(
                                id="expenses-table",
                                columns=[
                                    {"name": i, "id": i}
                                    for i in [
                                        "category",
                                        "cost",
                                        "note",
                                        "date",
                                        "currency",
                                        "account",
                                        "cost_euro",
                                    ]
                                ],
                                data=load_expenses().to_dict("records"),
                                style_table={
                                    "overflowX": "auto",
                                    "borderRadius": "8px",
                                },
                                style_header={
                                    "backgroundColor": colors["button"],
                                    "color": colors["text"],
                                    "fontWeight": "bold",
                                },
                                style_cell={
                                    "backgroundColor": colors["table_bg"],
                                    "color": colors["text"],
                                    "textAlign": "center",
                                    "padding": "10px",
                                },
                                style_filter={
                                    "backgroundColor": colors["text"],
                                    "color": colors["text"],
                                    "border": "1px solid " + colors["button"],
                                },
                                style_as_list_view=True,
                                page_size=10,  # Limit to 10 rows
                                sort_action="native",
                                filter_action="native",
                            ),
                        ],
                        style={
                            "backgroundColor": colors["block"],
                            "padding": "20px",
                            "borderRadius": "8px",
                        },
                    ),
                ],
                style={
                    "width": "48%",
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "padding": "20px",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Expenses by Category",
                                style={
                                    "color": colors["subtitle"],
                                    "textAlign": "center",
                                    "fontSize": "30px",
                                    "marginBottom": "5px",
                                    "marginTop": "5px",
                                },
                            ),
                            dcc.Graph(
                                id="category-summary",
                                style={"height": "440px", "borderRadius": "8px"},
                            ),
                        ],
                        style={
                            "backgroundColor": colors["block"],
                            "padding": "20px",
                            "borderRadius": "8px",
                            "marginBottom": "20px",
                        },
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Monthly Expenses by Category",
                                style={
                                    "color": colors["subtitle"],
                                    "textAlign": "center",
                                    "fontSize": "30px",
                                    "marginBottom": "5px",
                                    "marginTop": "5px",
                                },
                            ),
                            dcc.Graph(
                                id="monthly-summary",
                                style={"height": "478px", "borderRadius": "8px"},
                            ),
                        ],
                        style={
                            "backgroundColor": colors["block"],
                            "padding": "20px",
                            "borderRadius": "8px",
                        },
                    ),
                ],
                style={
                    "width": "48%",
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "padding": "20px",
                },
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
        },
    )

    return container_style, button_style, app_content


@app.callback(
    Output("expenses-table", "data"),
    Output("category-summary", "figure"),
    Output("monthly-summary", "figure"),
    Output("statistics-output", "children"),
    Output("income-update-message", "children"),
    Output("error-message", "children"),
    Input("add-expense-button", "n_clicks"),
    Input("set-income-button", "n_clicks"),
    State("input-category", "value"),
    State("input-cost", "value"),
    State("input-note", "value"),
    State("input-date", "date"),
    State("input-currency", "value"),
    State("input-account", "value"),
    State("input-monthly-income", "value"),
    State("input-income-currency", "value"),
    State("expenses-table", "data"),
)
def update_expenses(
    add_expense_clicks,
    set_income_clicks,
    category,
    cost,
    note,
    date,
    currency,
    account,
    monthly_income,
    income_currency,
    data,
):
    df = pd.DataFrame(data)

    # Handle income update
    income_update_message = ""
    if set_income_clicks > 0:
        if monthly_income is None or income_currency is None:
            income_update_message = "Please provide both income amount and currency."

    # Handle adding a new expense
    if add_expense_clicks > 0:
        if not category or cost is None or not date or not currency or not account:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                income_update_message,
                "Error: Please fill in all required fields.",
            )

        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                income_update_message,
                "Error: Invalid date format.",
            )

        expense_tracker.add_expense(
            category, cost, note, formatted_date, currency, account
        )

    df = load_expenses()
    df = convert_to_euro(df)

    if df.empty or not all(
        col in df.columns
        for col in [
            "category",
            "cost",
            "note",
            "date",
            "currency",
            "account",
            "cost_euro",
        ]
    ):
        return [], {}, {}, "", income_update_message, "No expenses to display."

    # Create category summary figure
    category_summary = df.groupby("category")["cost_euro"].sum().reset_index()
    category_figure = {
        "data": [
            {
                "x": category_summary["category"],
                "y": category_summary["cost_euro"],
                "type": "bar",
                "marker": {
                    "color": colors["button"],
                    "line": {"width": 0},  # No outline
                },
                "text": category_summary["cost_euro"],  # Add value labels
                "textposition": "outside",  # Position labels outside
            }
        ],
        "layout": {
            "plot_bgcolor": colors["block"],
            "paper_bgcolor": colors["block"],
            "font": {"color": colors["text"]},
            "yaxis": {
                "range": [0, category_summary["cost_euro"].max() * 1.2]
            },  # Increase y-axis limit
            "barmode": "group",
        },
    }

    # Create monthly summary figure
    df["month_year"] = pd.to_datetime(df["date"], format="%d-%m-%Y").dt.strftime(
        "%B %Y"
    )
    monthly_summary = (
        df.groupby(["month_year", "category"])["cost_euro"].sum().reset_index()
    )
    total_monthly_cost = df.groupby("month_year")["cost_euro"].sum().reset_index()

    category_colors = {
        category: color_palette[i % len(color_palette)]
        for i, category in enumerate(monthly_summary["category"].unique())
    }

    monthly_figure = {
        "data": [
            {
                "x": monthly_summary[monthly_summary["category"] == category][
                    "month_year"
                ],
                "y": monthly_summary[monthly_summary["category"] == category][
                    "cost_euro"
                ],
                "type": "bar",
                "name": category,
                "marker": {
                    "color": category_colors[category],
                    "line": {"width": 0},  # No outline
                },
            }
            for category in monthly_summary["category"].unique()
        ],
        "layout": {
            "plot_bgcolor": colors["block"],
            "paper_bgcolor": colors["block"],
            "font": {"color": colors["text"]},
            "barmode": "stack",
            "yaxis": {
                "range": [0, total_monthly_cost["cost_euro"].max() * 1.2]
            },  # Increase y-axis limit
            "annotations": [
                {
                    "x": row["month_year"],
                    "y": row["cost_euro"],
                    "text": f"{row['cost_euro']:.2f}",
                    "showarrow": False,
                    "font": {"color": colors["text"]},
                    "yanchor": "bottom",
                }
                for _, row in total_monthly_cost.iterrows()
            ],
        },
    }

    # Compute statistics
    if monthly_income is None:
        total_income = 0
    else:
        total_income = monthly_income * df["month_year"].nunique()

    total_expenses = df["cost_euro"].sum()
    total_profit_loss = total_income - total_expenses

    monthly_expenses = df.groupby("month_year")["cost_euro"].sum()
    mean_expenses = monthly_expenses.mean()

    # Handle the case where monthly_income is None
    if monthly_income is None:
        profit_loss_by_month = (
            monthly_expenses * 0
        )  # Set profit/loss to zero if no income is provided
    else:
        profit_loss_by_month = monthly_income - monthly_expenses

    mean_profit_loss = profit_loss_by_month.mean()

    statistics_output = html.Table(
        children=[
            html.Tr([html.Td("Total Income:"), html.Td(f"{total_income:.2f} €")]),
            html.Tr([html.Td("Total Expenses:"), html.Td(f"{total_expenses:.2f} €")]),
            html.Tr(
                [html.Td("Total Profit/Loss:"), html.Td(f"{total_profit_loss:.2f} €")]
            ),
            html.Tr(
                [html.Td("Mean Monthly Expenses:"), html.Td(f"{mean_expenses:.2f} €")]
            ),
            html.Tr(
                [
                    html.Td("Mean Monthly Profit/Loss:"),
                    html.Td(f"{mean_profit_loss:.2f} €"),
                ]
            ),
        ],
        style={
            "width": "90%",
            "margin": "0 auto",
            "color": colors["text"],
            "textAlign": "left",
            "borderCollapse": "collapse",
            "fontSize": "20px",
        },
        className="statistics-table",
    )

    return (
        df.to_dict("records"),
        category_figure,
        monthly_figure,
        statistics_output,
        income_update_message,
        "",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
