from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm, FilterForm


# Create your views here.
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
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

    if (request.GET == {}) or ("clear_filters" in request.GET):
        print("this is initial")
        print(request.GET)
        user = request.user
        expenses = Expense.objects.filter(user=request.user)
        categories = user.expense_set.values_list(
            "category__name", flat=True
        ).distinct()

        form = FilterForm(user=request.user)

        return render(
            request,
            "expenses/list_expenses.html",
            {"expenses": expenses, "categories": categories, "form": form},
        )
    elif "filter" in request.GET:
        print("this is with filters")
        print(request.GET)
        user = request.user
        expenses = Expense.objects.filter(user=request.user)
        form = FilterForm(request.GET, user=request.user)

        # Get filter values from request
        selected_categories = request.GET.getlist(
            "category"
        )  # Get multiple selected categories
        min_amount = request.GET.get("min_amount")
        max_amount = request.GET.get("max_amount")
        start_date = request.GET.get("from_date")
        end_date = request.GET.get("to_date")

        # Apply filters if values are provided
        if selected_categories:
            expenses = expenses.filter(
                category__name__in=selected_categories
            )  # Filter by multiple categories
        if min_amount:
            expenses = expenses.filter(amount__gte=min_amount)
        if max_amount:
            expenses = expenses.filter(amount__lte=max_amount)
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        categories = user.expense_set.values_list(
            "category__name", flat=True
        ).distinct()

        return render(
            request,
            "expenses/list_expenses.html",
            {
                "expenses": expenses,
                "categories": categories,
                "selected_categories": selected_categories,
                "form": form,
            },
        )
    elif "sort" in request.GET:
        sort_by = request.GET.get("sort-by")
        form = FilterForm(user=request.user)

        match sort_by:
            case "title":
                sorted_expenses = Expense.objects.filter(user=request.user).order_by(
                    "title"
                )
            case "amount":
                sorted_expenses = Expense.objects.filter(user=request.user).order_by(
                    "amount"
                )
            case "category":
                sorted_expenses = Expense.objects.filter(user=request.user).order_by(
                    "category__name"
                )
            case "date":
                sorted_expenses = Expense.objects.filter(user=request.user).order_by(
                    "date"
                )
            case "":
                sorted_expenses = Expense.objects.filter(user=request.user)

        return render(
            request,
            "expenses/list_expenses.html",
            {"expenses": sorted_expenses, "sort_by": sort_by, "form": form},
        )

    elif "search" in request.GET:
        ...


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
