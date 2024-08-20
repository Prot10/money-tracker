"""Module to create the Dash app for the Expense Tracker."""

import base64
from datetime import datetime

import dash
import pandas as pd
from dash import Input, Output, State, dcc, html

from .config import color_palette, dark_mode_colors, light_mode_colors
from .content import create_app_content
from .data.tracker import ExpenseTracker
from .utils import (
    convert_income_to_euro,
    convert_to_euro,
    ensure_csv_exists,
    load_expenses,
)

colors = dark_mode_colors

# Ensure the CSV file exists
ensure_csv_exists()

# Initialize the ExpenseTracker
expense_tracker = ExpenseTracker()

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Nunito&display=swap",
        "/assets/style.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    ],
)

style = {
    "backgroundColor": colors["background"],
    "fontFamily": "'Nunito', cursive",
    "margin": "0",
    "padding": "0",
    "minHeight": "100vh",
    "position": "relative",
}

buttons_style = {
    "position": "absolute",
    "top": "10px",
    "right": "10px",
    "backgroundColor": colors["button"],
    "color": colors["subtitle"],
    "borderRadius": "5px",
    "padding": "10px",
    "fontSize": "15px",
}

# Layout of the app
app.layout = html.Div(
    id="main-container",
    style=style,
    children=[
        html.Button(
            "Toggle Light/Dark Mode",
            id="toggle-button",
            style=buttons_style,
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                [
                    html.I(
                        className="fas fa-upload",
                        style={"fontSize": "24px", "marginRight": "10px"},
                    ),
                    "Upload CSV File",
                ]
            ),
            style={
                "width": "10%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "left",
                "margin": "10px",
            },
            multiple=True,
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
        create_app_content(colors, expense_tracker),
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
    if n_clicks is None or n_clicks % 2 == 0:
        colors = dark_mode_colors
    else:
        colors = light_mode_colors

    container_style = style

    button_style = buttons_style

    app_content = (create_app_content(colors, expense_tracker),)

    return container_style, button_style, app_content


@app.callback(
    # Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        for content, name in zip(list_of_contents, list_of_names):
            # Save the uploaded content to a temporary file
            content_type, content_string = content.split(",")
            decoded = base64.b64decode(content_string)
            with open(name, "wb") as f:
                f.write(decoded)

            # Create an instance of ExpenseTracker with the uploaded file
            tracker = ExpenseTracker(name)

            # Check the CSV columns
            try:
                tracker.check_csv_columns()
                # Load expenses if the check is successful
                tracker._load_expenses()
                return f"Successfully loaded {name} with required columns."
            except ValueError as e:
                return str(e)


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

    df = load_expenses(expense_tracker)
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
                "text": category_summary["cost_euro"].apply(lambda x: f"{x:.2f}"),
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

    monthly_summary = monthly_summary.sort_values(by="month_year", ascending=False)

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
                    "line": {"width": 0},
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
        monthly_income_euro = convert_income_to_euro(monthly_income, income_currency)
        total_income = monthly_income_euro * df["month_year"].nunique()

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
            html.Tr(
                [
                    html.Td("Total Income:", style={"padding": "10px"}),
                    html.Td(f"{total_income:.2f} €", style={"padding": "10px"}),
                ]
            ),
            html.Tr(
                [
                    html.Td("Total Expenses:", style={"padding": "10px"}),
                    html.Td(f"{total_expenses:.2f} €", style={"padding": "10px"}),
                ]
            ),
            html.Tr(
                [
                    html.Td("Total Profit/Loss:", style={"padding": "10px"}),
                    html.Td(f"{total_profit_loss:.2f} €", style={"padding": "10px"}),
                ]
            ),
            html.Tr(
                [
                    html.Td("Mean Monthly Expenses:", style={"padding": "10px"}),
                    html.Td(f"{mean_expenses:.2f} €", style={"padding": "10px"}),
                ]
            ),
            html.Tr(
                [
                    html.Td("Mean Monthly Profit/Loss:", style={"padding": "10px"}),
                    html.Td(f"{mean_profit_loss:.2f} €", style={"padding": "10px"}),
                ]
            ),
        ],
        style={
            "width": "90%",
            "margin": "0 auto",
            "color": colors["text"],
            "textAlign": "left",
            "borderCollapse": "collapse",
            "fontSize": "15px",
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
