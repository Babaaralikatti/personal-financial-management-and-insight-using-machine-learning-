import django_filters
from .models import Income_Record
from BAM.models import Accounts


class IncomeRecordFilter(django_filters.FilterSet):
    account = django_filters.ModelChoiceFilter(
        queryset=lambda request: Accounts.objects.filter(user=request.user)
    )
    category = django_filters.ModelChoiceFilter(
        queryset=lambda request: request.user.income_category_set.all()
    )
    date = django_filters.DateRangeFilter()
    amount = django_filters.RangeFilter()

    class Meta:
        model = Income_Record
        fields = ["account", "category", "date", "amount"]
