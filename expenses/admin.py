from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "predefined",
    )  # Show these fields in the admin list view
    list_filter = (
        "predefined",
    )  # Add filter to separate predefined and user-defined categories
    search_fields = ("name",)  # Enable search by category name


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "amount",
        "category",
        "date",
        "created_at",
    )  # Display important fields
    list_filter = ("category", "date")  # Filters for easier navigation
    search_fields = (
        "title",
        "category__name",
    )  # Enable search by expense title or category name
