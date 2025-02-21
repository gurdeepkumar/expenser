from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm


# Create your views here.
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            print(form.cleaned_data)
            expense = form.save(commit=False)
            expense.user = request.user  # Assign expense to logged-in user

            # Handle new category if provided
            category_name = form.cleaned_data.get("category")
            new_category_name = form.cleaned_data.get("new_category")
            if category_name == None:
                if (
                    Category.objects.filter(
                        name=new_category_name, predefined=True
                    ).exists()
                ) or (
                    Category.objects.filter(
                        name=new_category_name, user=request.user
                    ).exists()
                ):
                    category = new_category_name
                else:
                    category, created = Category.objects.get_or_create(
                        name=new_category_name, user=request.user, predefined=False
                    )
            else:
                if Category.objects.filter(
                    name=category_name, predefined=True
                ).exists() or (
                    Category.objects.filter(
                        name=category_name, user=request.user
                    ).exists()
                ):
                    category = category_name

            expense.category = category
            expense.save()
            return redirect("list_expenses")  # Redirect after saving
    else:
        form = ExpenseForm(user=request.user)  # Pass user to form

    return render(request, "expenses/add_expense.html", {"form": form})


@login_required
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, "expenses/list_expenses.html", {"expenses": expenses})


@login_required
def view_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        # Handle deletion of the expense
        expense.delete()
        return redirect("list_expenses")  # Redirect to the expense list after deletion

    return render(request, "expenses/view_expense.html", {"expense": expense})


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(
                "view_expense", expense_id=expense.id
            )  # Redirect to the view expense page after editing
    else:
        form = ExpenseForm(instance=expense, user=request.user)

    return render(
        request, "expenses/edit_expense.html", {"form": form, "expense": expense}
    )
