from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
import json
from django.urls import resolve


# Create your views here.
@login_required
def home(request):
    current_url_name = resolve(request.path_info).url_name  # Get the current URL name

    expenses = Expense.objects.filter(user=request.user)
    # for pie chart
    # Group expenses by category and sum the amounts
    category_data = {}
    for expense in expenses:
        category_data[expense.category.name] = category_data.get(
            expense.category.name, 0
        ) + float(expense.amount)

    # Convert data to JSON for use in JavaScript
    chart_labels = list(category_data.keys())
    chart_values = list(category_data.values())

    # for bar chart
    # Aggregate total spending per month
    monthly_data = {}
    for expense in expenses:
        month = expense.date.strftime("%Y-%m")  # Format: YYYY-MM (e.g., 2025-01)
        monthly_data[month] = monthly_data.get(month, 0) + float(
            expense.amount
        )  # Convert Decimal to float

    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())

    # Prepare data for Chart.js
    chart_labels_bar = sorted_months
    chart_values_bar = [monthly_data[month] for month in sorted_months]

    # for line chart
    # Aggregate total spending per day
    daily_data = {}
    for expense in expenses:
        day = expense.date.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        daily_data[day] = daily_data.get(day, 0) + float(
            expense.amount
        )  # Convert Decimal to float

    # Sort dates chronologically
    sorted_days = sorted(daily_data.keys())

    # Prepare data for Chart.js
    chart_labels_line = sorted_days
    chart_values_line = [daily_data[day] for day in sorted_days]

    context = {
        "chart_labels": json.dumps(chart_labels),
        "chart_values": json.dumps(chart_values),
        "chart_labels_bar": json.dumps(chart_labels_bar),
        "chart_values_bar": json.dumps(chart_values_bar),
        "chart_labels_line": json.dumps(chart_labels_line),
        "chart_values_line": json.dumps(chart_values_line),
        "expenses": expenses,
        "show_welcome": current_url_name == "home",  # Show welcome text only on home
        "show_chart": True,  # Show chart on both pages
    }

    return render(request, "core/home.html", context)
