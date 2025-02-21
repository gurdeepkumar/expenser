from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_expenses, name="list_expenses"),
    path("add", views.add_expense, name="add_expenses"),
    path("<int:expense_id>/", views.view_expense, name="view_expense"),
    path(
        "edit/<int:expense_id>/", views.edit_expense, name="edit_expense"
    ),  # Add this line
]
