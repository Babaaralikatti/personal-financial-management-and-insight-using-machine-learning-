from django.urls import path
from .views import *

urlpatterns = [
    path("add-new-account/", add_new_account_form_view, name="add_new_account"),
    path("update-account/<int:pk>/", update_account_form_view, name="update_account"),
    path("account-list/", AccountBalanceListView.as_view(), name="account_list"),
    path(
        "transfer/",
        add_new_inter_account_transaction_record_view,
        name="inter_account_transaction",
    ),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
