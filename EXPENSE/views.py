from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pandas as pd
from .filters import ExpenseRecordFilter
from .models import Expense_Record, Expense_Category
from .forms import ExpenseRecordForm, ExpenseCategoryForm
from BAM.models import Accounts


# Create your views here.
@login_required
def add_expense_record_view(request):
    user = request.user
    form = ExpenseRecordForm(user, request.POST or None)
    if form.is_valid():
        account = Accounts.objects.get(pk=form.data["account"])
        account.account_balance = account.account_balance - float(form.data["amount"])
        account.last_update_date = datetime.datetime.now()
        account.save()
        form.save()
        form = ExpenseRecordForm(user)

    context = {"form": form}
    return render(request, "expense/expense_form.html", context)


@login_required
def add_expense_category_view(request):
    form = ExpenseCategoryForm(request.POST or None)
    if form.is_valid():
        Expanse_Category = form.save(commit=False)
        Expanse_Category.user = request.user
        Expanse_Category.save()
        return redirect("expanse-category-list")

    context = {"form": form}
    return render(request, "expense/expense_form.html", context)


@login_required
def update_expanse_category_view(request, pk):
    category = Expense_Category.objects.get(pk=pk)
    form = ExpenseCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("expanse-category-list")

    context = {"form": form}
    return render(request, "expense/expense_form.html", context)


@login_required
def update_expanse_record_view(request, pk):
    record = Expense_Record.objects.get(pk=pk)
    user = request.user
    form = ExpenseRecordForm(user, request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect("expanse-record-list")

    context = {"form": form}
    return render(request, "expense/expense_form.html", context)


class ExpanseCategoryList(LoginRequiredMixin, ListView):
    model = Expense_Category
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = context["object_list"].filter(user=self.request.user)
        return context


import os
from django.conf import settings
import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render

import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render


def expense_record_list(request):
    # Path to the CSV file
    csv_file_path = r"C:\Users\Asus\OneDrive\Documents\GitHub\Final-Year-Project\AIFMS\static\data\MyTransaction.csv"

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Clean up column names (remove extra spaces)
        df.columns = df.columns.str.strip()

        # Ensure 'Date' is in datetime format
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

            # Drop rows where 'Date' is NaT (invalid date values)
            df = df.dropna(subset=["Date"])

            # Format the 'Date' column to show only the date part (no time)
            df["Date"] = df["Date"].dt.date

            # Sort the DataFrame by 'Date' in descending order (newest first)
            df_sorted = df.sort_values(by="Date", ascending=False)

            # Select the relevant columns
            required_columns = ["Date", "Category", "Withdrawal", "Deposit", "Balance"]
            records = df_sorted[required_columns].to_dict(orient="records")

        else:
            records = []

    except FileNotFoundError:
        records = []

    # Pagination setup
    paginator = Paginator(records, 10)  # Show 10 records per page
    page_number = request.GET.get(
        "page"
    )  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object

    return render(request, "EXPENSE/expense_record_list.html", {"page_obj": page_obj})
