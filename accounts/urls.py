from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import (
    CustomPasswordChangeView,
    CustomLoginView,
    RegistrationView,
    delete_user,
    generate_api,
)


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("update/", CustomPasswordChangeView.as_view(), name="password_change"),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("delete-user/", delete_user, name="delete_user"),
    path("generate-api/", generate_api, name="generate_api"),
]
