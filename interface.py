from datetime import datetime

import dash
import pandas as pd
from dash import Input, Output, State, dash_table, dcc, html

from tracker import CSV_PATH, ExpenseTracker


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
app = dash.Dash(__name__)


# Load existing data
def load_expenses():
    df = pd.DataFrame([expense.dict() for expense in expense_tracker.get_expenses()])
    # Ensure that the DataFrame has the necessary columns
    if df.empty:
        df = pd.DataFrame(
            columns=["category", "cost", "note", "date", "currency", "account"]
        )
    return df


# Define the color palette
colors = {
    "background": "#3F334D",  # Background color
    "text": "#FFFFFF",  # White text
    "block": "#7D8491",  # Block background
    "input_block": "#7D8491",  # Input commands block
    "button": "#574B60",  # Button and table header
    "table_bg": "#C0C5C1",  # Table background
}

# Create a palette excluding the block background color
color_palette = [
    colors["text"],  # White text
    colors["button"],  # Button color
    colors["table_bg"],  # Table background
]

# Add additional colors to match the style
additional_colors = [
    "#FF6F61",  # Coral
    "#6B5B95",  # Purple
    "#88B04B",  # Green
    "#F7CAC9",  # Pink
    "#92A8D1",  # Blue
]

# Combine the existing and additional colors
color_palette.extend(additional_colors)

# Layout of the app
app.layout = html.Div(
    style={"backgroundColor": colors["background"], "fontFamily": "Arial, sans-serif"},
    children=[
        html.H1(
            "Expense Tracker",
            style={"textAlign": "center", "color": colors["text"], "padding": "20px"},
        ),
        html.Div(
            [
                # Column 1
                html.Div(
                    [
                        # First Block: Menu to insert a new item
                        html.Div(
                            [
                                html.H3(
                                    "Add New Expense",
                                    style={
                                        "color": colors["text"],
                                        "textAlign": "center",
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
                                            },
                                        ),
                                        dcc.Input(
                                            id="input-note",
                                            type="text",
                                            value="",
                                            placeholder="e.g., Lunch with friends (Optional)",
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
                                            "Date",
                                            style={
                                                "color": colors["text"],
                                                "display": "block",
                                                "textAlign": "center",
                                            },
                                        ),
                                        dcc.DatePickerSingle(
                                            id="input-date",
                                            date=datetime.now().strftime("%Y-%m-%d"),
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
                                            },
                                        ),
                                        dcc.Input(
                                            id="input-currency",
                                            type="text",
                                            value="EUR",
                                            placeholder="e.g., EUR",
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
                                            "Account",
                                            style={
                                                "color": colors["text"],
                                                "display": "block",
                                                "textAlign": "center",
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
                                        "width": "60%",
                                        "margin": "10px auto",
                                        "backgroundColor": colors["button"],
                                        "color": colors["text"],
                                        "borderRadius": "5px",
                                        "display": "block",
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
                                "backgroundColor": colors["input_block"],
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        # Second Block: Table with all expenses
                        html.Div(
                            [
                                html.H3(
                                    "Expenses",
                                    style={
                                        "color": colors["text"],
                                        "textAlign": "center",
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
                # Column 2
                html.Div(
                    [
                        # First Block: Interactive barplot for categories
                        html.Div(
                            [
                                html.H3(
                                    "Expenses by Category",
                                    style={
                                        "color": colors["text"],
                                        "textAlign": "center",
                                    },
                                ),
                                dcc.Graph(
                                    id="category-summary",
                                    style={"height": "358px", "borderRadius": "8px"},
                                ),
                            ],
                            style={
                                "backgroundColor": colors["block"],
                                "padding": "20px",
                                "borderRadius": "8px",
                                "marginBottom": "20px",
                            },
                        ),
                        # Second Block: Barplot for monthly expenses by category
                        html.Div(
                            [
                                html.H3(
                                    "Monthly Expenses by Category",
                                    style={
                                        "color": colors["text"],
                                        "textAlign": "center",
                                    },
                                ),
                                dcc.Graph(
                                    id="monthly-summary",
                                    style={"height": "358px", "borderRadius": "8px"},
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
            style={"display": "flex", "justifyContent": "space-between"},
        ),
    ],
)


# Callback to add an expense and update graphs
@app.callback(
    Output("expenses-table", "data"),
    Output("category-summary", "figure"),
    Output("monthly-summary", "figure"),
    Output("error-message", "children"),
    Input("add-expense-button", "n_clicks"),
    State("input-category", "value"),
    State("input-cost", "value"),
    State("input-note", "value"),
    State("input-date", "date"),
    State("input-currency", "value"),
    State("input-account", "value"),
    State("expenses-table", "data"),
)
def update_expenses(n_clicks, category, cost, note, date, currency, account, data):
    df = pd.DataFrame(data)

    # Handle adding a new expense
    if n_clicks > 0:
        if not category or cost is None or not date or not currency or not account:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                "Error: Please fill in all required fields.",
            )

        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                "Error: Invalid date format.",
            )

        expense_tracker.add_expense(
            category, cost, note, formatted_date, currency, account
        )

    df = load_expenses()

    # Ensure DataFrame has required columns
    if df.empty or not all(
        col in df.columns
        for col in ["category", "cost", "note", "date", "currency", "account"]
    ):
        return [], {}, {}, "No expenses to display."

    # Create category summary figure
    category_summary = df.groupby("category")["cost"].sum().reset_index()
    category_figure = {
        "data": [
            {
                "x": category_summary["category"],
                "y": category_summary["cost"],
                "type": "bar",
                "marker": {
                    "color": colors["button"],
                    "line": {"width": 0},  # No outline
                },
                "text": category_summary["cost"],  # Add value labels
                "textposition": "outside",  # Position labels outside
            }
        ],
        "layout": {
            "plot_bgcolor": colors["block"],
            "paper_bgcolor": colors["block"],
            "font": {"color": colors["text"]},
            "yaxis": {
                "range": [0, category_summary["cost"].max() * 1.2]
            },  # Increase y-axis limit
            "barmode": "group",
        },
    }

    # Create monthly summary figure
    df["month_year"] = pd.to_datetime(df["date"], format="%d-%m-%Y").dt.strftime(
        "%B %Y"
    )  # Convert to "Month Year" format
    monthly_summary = df.groupby(["month_year", "category"])["cost"].sum().reset_index()

    # Calculate total cost per month
    total_monthly_cost = df.groupby("month_year")["cost"].sum().reset_index()

    # Assign colors to categories using the palette
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
                "y": monthly_summary[monthly_summary["category"] == category]["cost"],
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
                "range": [0, total_monthly_cost["cost"].max() * 1.2]
            },  # Increase y-axis limit
            "annotations": [
                {
                    "x": row["month_year"],
                    "y": row["cost"],
                    "text": f"{row['cost']:.2f}",  # Display total cost with two decimal places
                    "showarrow": False,
                    "font": {"color": colors["text"]},
                    "yanchor": "bottom",
                }
                for _, row in total_monthly_cost.iterrows()
            ],
        },
    }
    return df.to_dict("records"), category_figure, monthly_figure, ""


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
