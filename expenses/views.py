from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Category
from .forms import ExpenseForm, RefiningForm, SearchForm, SortForm
from django.db.models import Q
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user).select_related("category")
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDetailView(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return None

    def get(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(
                {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return None

    def put(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(
                {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return None

    def delete(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(
                {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
            )

        expense.delete()
        return Response(
            {"message": "Expense deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


@login_required
def list_expenses(request):
    user = request.user
    categories = user.expense_set.values_list("category__name", flat=True).distinct()

    if request.GET == {} or ("clear_filters" in request.GET):
        expenses = (
            Expense.objects.filter(user=request.user)
            .order_by("-created_at")
            .select_related("category")
        )
        search_form = SearchForm()
        sort_form = SortForm()
        filter_form = RefiningForm(user=request.user)
        total_expenses = sum(expense.amount for expense in expenses)

        return render(
            request,
            "expenses/list_expenses.html",
            {
                "expenses": expenses,
                "categories": categories,
                "total_expenses": total_expenses,
                "search_form": search_form,
                "sort_form": sort_form,
                "filter_form": filter_form,
            },
        )
    elif "filter" in request.GET:
        filter_expenses = Expense.objects.filter(user=request.user)
        search_form = SearchForm()
        sort_form = SortForm()
        filter_form = RefiningForm(request.GET, user=request.user)

        # Get filter values from request
        selected_categories_ids = request.GET.getlist(
            "category"
        )  # Get multiple selected categories
        min_amount = request.GET.get("min_amount")
        max_amount = request.GET.get("max_amount")
        start_date = request.GET.get("from_date")
        end_date = request.GET.get("to_date")
        # Apply filters if values are provided
        if selected_categories_ids:
            selected_categories = []
            for category_id in selected_categories_ids:
                selected_categories.append(
                    Category.objects.filter(id=category_id).first()
                )
            filter_expenses = filter_expenses.filter(
                category__name__in=selected_categories
            )  # Filter by multiple categories
        if min_amount:
            filter_expenses = filter_expenses.filter(amount__gte=min_amount)
        if max_amount:
            filter_expenses = filter_expenses.filter(amount__lte=max_amount)
        if start_date:
            filter_expenses = filter_expenses.filter(date__gte=start_date)
        if end_date:
            filter_expenses = filter_expenses.filter(date__lte=end_date)

        total_expenses = sum(expense.amount for expense in filter_expenses)

        return render(
            request,
            "expenses/list_expenses.html",
            {
                "expenses": filter_expenses,
                "categories": categories,
                "total_expenses": total_expenses,
                "search_form": search_form,
                "sort_form": sort_form,
                "filter_form": filter_form,
            },
        )
    elif "sort" in request.GET:
        sort_by = request.GET.get("sort_by")
        sort_order = request.GET.get("sort_order")
        search_form = SearchForm()
        sort_form = SortForm(request.GET)
        filter_form = RefiningForm(user=request.user)

        match sort_by:
            case "title":
                if sort_order == "ascending":
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("title")
                else:
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("-title")
            case "amount":
                if sort_order == "ascending":
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("amount")
                else:
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("-amount")
            case "category":
                if sort_order == "ascending":
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("category__name")
                else:
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("-category__name")
            case "date":
                if sort_order == "ascending":
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("date")
                else:
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("-date")
            case "":
                if sort_order == "ascending":
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("created_at")
                else:
                    sorted_expenses = Expense.objects.filter(
                        user=request.user
                    ).order_by("-created_at")

        total_expenses = sum(expense.amount for expense in sorted_expenses)

        return render(
            request,
            "expenses/list_expenses.html",
            {
                "expenses": sorted_expenses,
                "categories": categories,
                "sort_order": sort_order,
                "sort_by": sort_by,
                "total_expenses": total_expenses,
                "search_form": search_form,
                "sort_form": sort_form,
                "filter_form": filter_form,
            },
        )

    elif "search" in request.GET:
        expenses = Expense.objects.filter(user=request.user)
        search_form = SearchForm(request.GET)
        sort_form = SortForm()
        filter_form = RefiningForm(user=request.user)

        search_input = request.GET.get("search_input")
        searched_expenses = expenses.filter(
            Q(title__icontains=search_input) | Q(category__name__icontains=search_input)
        )

        total_expenses = sum(expense.amount for expense in searched_expenses)

        return render(
            request,
            "expenses/list_expenses.html",
            {
                "expenses": searched_expenses,
                "categories": categories,
                "search_input": search_input,
                "total_expenses": total_expenses,
                "search_form": search_form,
                "sort_form": sort_form,
                "filter_form": filter_form,
            },
        )


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
            expense.user = request.user

            duplicate_expense = Expense.objects.filter(
                user=request.user,
                title=expense.title,
                amount=expense.amount,
                category=expense.category,
                date=expense.date,
            ).exists()

            if duplicate_expense:
                messages.error(request, "This expense already exists!")
                return render(request, "expenses/add_expense.html", {"form": form})

            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect("list_expenses")
    else:
        form = ExpenseForm(user=request.user)

    return render(request, "expenses/add_expense.html", {"form": form})


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
