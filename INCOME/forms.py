from django import forms
from .models import Income_Record, Income_Category
from BAM.models import Accounts


class IncomeRecordForm(forms.ModelForm):
    class Meta:
        model = Income_Record
        fields = ("account", "category", "amount", "details", "date")
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = Accounts.objects.filter(user=user)
        self.fields["category"].queryset = Income_Category.objects.filter(user=user)


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = Income_Category
        fields = ("category",)
