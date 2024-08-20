"""Module to create the content of the Dash app."""

from datetime import datetime

from dash import dash_table, dcc, html

from .utils import load_expenses


def create_app_content(colors, expense_tracker):
    """Function to create the content of the Dash app."""
    return html.Div(
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
                                                    "height": "30px",
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
                                                    "height": "30px",
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
                                                    "height": "30px",
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
                                                    "padding": "10px",  # Add padding
                                                    "color": "#333",  # Set text color
                                                    "fontSize": "16px",  # Set font size
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
                                                    "height": "30px",
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
                                                    "height": "30px",
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
                                            "margin": "20px auto",
                                            "backgroundColor": colors["button"],
                                            "color": colors["subtitle"],
                                            "borderRadius": "5px",
                                            "display": "block",
                                            "fontSize": "18px",
                                            "height": "35px",
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
                                                    "height": "30px",
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
                                                    "height": "30px",
                                                },
                                                clearable=False,
                                            ),
                                            html.Button(
                                                "Update Income",
                                                id="set-income-button",
                                                n_clicks=0,
                                                style={
                                                    "width": "40%",
                                                    "margin": "20px auto",
                                                    "backgroundColor": colors["button"],
                                                    "color": colors["subtitle"],
                                                    "borderRadius": "5px",
                                                    "display": "block",
                                                    "fontSize": "18px",
                                                    "height": "35px",
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
                                data=load_expenses(expense_tracker).to_dict("records"),
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
                                page_size=10,
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
                                style={"height": "518px", "borderRadius": "8px"},
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
