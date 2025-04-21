from django.urls import path
from DASHBOARD import views
from django.contrib.auth import views as auth_views
from ML_Models import views as ML_views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("home", views.dashboard_view, name="home"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views


