from django.contrib import admin
from django.urls import path, include
from requestsapp import views as app_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", app_views.login_view, name="login"),
    path("accounts/logout/", app_views.logout_view, name="logout"),
    path("accounts/signup/", app_views.signup, name="signup"),
    path("", include("requestsapp.urls")),
]
