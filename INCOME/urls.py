from django.urls import path
from .views import *

urlpatterns = [
    path("add-income-record/", add_income_record_view, name="add-income-record"),
    path("income-category-list/", CategoryList.as_view(), name="income-category-list"),
    path("income-record-list/", IncomeRecordList.as_view(), name="income-record-list"),
    path("add-income-category/", add_income_category_view, name="add-income-category"),
    path(
        "update-income-record/<int:pk>/",
        update_income_record_view,
        name="update-income-record",
    ),
    path(
        "update-income-category/<int:pk>/",
        update_income_category_view,
        name="update-income-category",
    ),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
