from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Income_Record, Income_Category
from .forms import IncomeRecordForm, IncomeCategoryForm
from BAM.models import Accounts
from .filters import IncomeRecordFilter
from datetime import datetime


@login_required
def add_income_record_view(request):
    user = request.user
    form = IncomeRecordForm(user, request.POST or None)
    if form.is_valid():
        account = form.cleaned_data["account"]
        account.account_balance += form.cleaned_data["amount"]
        account.last_update_date = datetime.now()
        account.save()
        form.save()
        return redirect("income-record-list")
    return render(request, "income/income_form.html", {"form": form})


@login_required
def add_income_category_view(request):
    form = IncomeCategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        return redirect("income-category-list")
    return render(request, "income/income_form.html", {"form": form})


@login_required
def update_income_record_view(request, pk):
    record = get_object_or_404(Income_Record, pk=pk)
    form = IncomeRecordForm(request.user, request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect("income-record-list")
    return render(request, "income/income_form.html", {"form": form})


@login_required
def update_income_category_view(request, pk):
    category = get_object_or_404(Income_Category, pk=pk)
    form = IncomeCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("income-category-list")
    return render(request, "income/income_form.html", {"form": form})


class CategoryList(LoginRequiredMixin, ListView):
    model = Income_Category
    template_name = "income/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class IncomeRecordList(LoginRequiredMixin, ListView):
    model = Income_Record
    template_name = "income/record_list.html"
    context_object_name = "records"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = context["records"].filter(account__user=self.request.user)
        context["filter"] = IncomeRecordFilter(
            self.request.GET,
            queryset=context["records"].select_related("category").order_by("-date"),
        )
        context["records"] = context["filter"].qs
        return context
