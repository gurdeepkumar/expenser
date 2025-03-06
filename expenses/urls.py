from django.urls import path, include
from . import views
from rest_framework.authtoken import views as auth_views
from .views import (
    ExpenseListView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
    ExpenseDetailView,
)


urlpatterns = [
    path("", views.list_expenses, name="list_expenses"),
    path("add", views.add_expense, name="add_expenses"),
    path("<int:expense_id>/", views.view_expense, name="view_expense"),
    path("edit/<int:expense_id>/", views.edit_expense, name="edit_expense"),
    path("api/expenses/", ExpenseListView.as_view(), name="expense-list"),
    path("api/expenses/create/", ExpenseCreateView.as_view(), name="expense-create"),
    path(
        "api/expenses/<int:pk>/update/",
        ExpenseUpdateView.as_view(),
        name="expense-update",
    ),
    path(
        "api/expenses/<int:pk>/delete/",
        ExpenseDeleteView.as_view(),
        name="expense-delete",
    ),
    path("api/token/", auth_views.obtain_auth_token),
    path("api/expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
]
