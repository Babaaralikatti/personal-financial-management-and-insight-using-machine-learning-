from django.shortcuts import render
import joblib
import pandas as pd
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Import the correct function
from ML_Models.predict import predict_savings_for_next_month


# Load the trained recommendation model once when the server starts
RECOMMENDATION_MODEL_PATH = "ML_Models/recommendation_model.pkl"
recommendation_model = joblib.load(RECOMMENDATION_MODEL_PATH)


def landing_page(request):
    return render(request, "DASHBOARD/landing_page.html")


@login_required
def dashboard_view(request):
    # Load the dataset
    df = pd.read_csv("static/data/MyTransaction.csv")

    # Ensure numeric conversion for 'Deposit' and 'Withdrawal'
    df["Deposit"] = pd.to_numeric(df["Deposit"] * 2.2, errors="coerce").fillna(0)
    df["Withdrawal"] = pd.to_numeric(df["Withdrawal"], errors="coerce").fillna(0)

    # Ensure the 'Date' column is parsed correctly and drop rows with invalid dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])  # Remove rows with NaT in 'Date'

    # Convert Date to string for template display
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    # Calculate Total Income and Expense
    total_income = df["Deposit"].sum()
    total_expense = df["Withdrawal"].sum()

    # Calculate Remaining Balance and Net Worth
    remaining_balance = total_income - total_expense
    net_worth = remaining_balance

    # Determine transaction type and amount for display
    df["Type"] = df.apply(lambda row: "-" if row["Withdrawal"] > 0 else "+", axis=1)
    df["Amount"] = df.apply(
        lambda row: row["Withdrawal"] if row["Withdrawal"] > 0 else row["Deposit"],
        axis=1,
    )

    # Prepare category data for pie chart
    category_summary = df.groupby("Category")[["Withdrawal"]].sum()
    category_labels = category_summary.index.tolist()
    category_values = category_summary["Withdrawal"].tolist()

    # Sort the DataFrame by Date in descending order
    df_sorted = df.sort_values(by="Date", ascending=False)

    # Process data for line chart (example: monthly income vs expenses)
    df.set_index(pd.to_datetime(df["Date"]), inplace=True)
    monthly_summary = df.resample("ME").agg(
        {"Deposit": "sum", "Withdrawal": "sum"}
    )  # Updated resample frequency
    months = monthly_summary.index.strftime("%b %Y").tolist()
    incomes = monthly_summary["Deposit"].tolist()
    expenses = monthly_summary["Withdrawal"].tolist()

    # Select relevant columns for the table display
    transaction_summary = (
        df_sorted[["Date", "Category", "Amount", "Type"]]
        .reset_index(drop=True)
        .to_dict(orient="records")
    )

    # Example of generating predictions using the ML model
    predicted_savings_result = (
        predict_savings_for_next_month()
    )  # Changed function name here

    # Recommendation Logic
    # Prepare data for the recommendation model
    user_data = pd.DataFrame(
        {
            "Total Income": [total_income],
            "Total Expense": [total_expense],
            "Remaining Balance": [remaining_balance],
        }
    )

    # Add category-specific spending
    for category, spending in zip(category_labels, category_values):
        user_data[category] = spending

    # Ensure all required features are present
    model_features = recommendation_model.feature_names_in_
    for feature in model_features:
        if feature not in user_data.columns:
            user_data[feature] = 0

    # Align columns with the model
    user_data = user_data[model_features]

    # Predict recommendations
    rec_label = recommendation_model.predict(user_data)[0]

    # Translate model output into actionable advice
    if rec_label == "save_more":
        recommendations = [
            "Cut down on unnecessary expenses in the following categories:",
            ", ".join(
                [
                    cat
                    for cat, spend in zip(category_labels, category_values)
                    if spend > (0.2 * total_expense)
                ]
            ),
            "Focus on essential spending to maximize your savings.",
        ]
    elif rec_label == "spend_more":
        recommendations = [
            "You have saved enough; consider increasing spending in the following categories:",
            ", ".join(
                [
                    cat
                    for cat, spend in zip(category_labels, category_values)
                    if spend < (0.1 * total_expense)
                ]
            ),
            "Invest or allocate funds towards personal development.",
        ]
    else:
        recommendations = ["Your spending is well balanced. Keep it up!"]

    # Implement pagination
    page = request.GET.get("page", 1)  # Get page number from request
    paginator = Paginator(transaction_summary, 10)  # Show 10 transactions per page

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(
            1
        )  # If page is not an integer, deliver first page.
    except EmptyPage:
        transactions_page = paginator.page(
            paginator.num_pages
        )  # If page is out of range, deliver last page.

    # Consolidated context dictionary
    context = {
        "income_data": total_income,
        "net_worth": net_worth,
        "expense_data": total_expense,
        "remaining_balance": remaining_balance,
        "transaction_summary": transactions_page,
        "df_sorted": df_sorted,
        "category_labels": json.dumps(category_labels),
        "category_values": json.dumps(category_values),
        "months": json.dumps(months),
        "incomes": json.dumps(incomes),
        "expenses": json.dumps(expenses),
        "predicted_savings": predicted_savings_result,  # Added prediction result
        "recommendations": recommendations,  # Added recommendations
    }

    return render(request, "DASHBOARD/home.html", context)


# Including DATASET function


def parse_mixed_dates(date_series):
    try:
        # Automatically handle mixed date formats with dayfirst set to True
        return pd.to_datetime(date_series, dayfirst=True, errors="coerce")
    except ValueError:
        # Handle any remaining issues (you can also log the errors for further debugging)
        return pd.NaT

from django.shortcuts import render

# Initialize budget variables
budget_data = {
    "goal": 1000.00,
    "used": 0.00,
}

def budget_goal_view(request):
    global budget_data

    if request.method == "POST":
        # Get user input from the form
        goal = request.POST.get("goal")
        used = request.POST.get("used")

        # Validate and update the budget data
        if goal:
            budget_data["goal"] = float(goal)
        if used:
            budget_data["used"] = float(used)

    # Pass the budget data to the template
    context = {
        "goal": budget_data["goal"],
        "used": budget_data["used"],
    }
    return render(request, "budget_goal.html", context)
from django.shortcuts import render, redirect
from .models import Budget
from .forms import BudgetForm

def budget_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    else:
        form = BudgetForm(instance=budget)

    context = {
        'budget': budget,
        'form': form,
    }
    return render(request, 'budget.html', context)
