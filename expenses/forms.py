from django import forms
from .models import Expense, Category


class SearchForm(forms.Form):
    search_input = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )


class SortForm(forms.Form):
    sort_types = [
        ("", "Created On"),
        ("title", "Title"),
        ("amount", "Amount"),
        ("category", "Category"),
        ("date", "Expense Date"),
    ]

    sort_by = forms.ChoiceField(
        choices=sort_types,
        required=False,
        label="sort_by",
    )

    sort_order_types = [
        ("decending", "Decending"),
        ("ascending", "Ascending"),
    ]

    sort_order = forms.ChoiceField(
        choices=sort_order_types,
        required=False,
        label="sort_order",
    )


class RefiningForm(forms.Form):
    min_amount = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Max Amount"}),
    )
    max_amount = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Min Amount"}),
    )
    from_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    to_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Fetch predefined categories + categories created by the user + sorting fields
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(
                predefined=True
            ) | Category.objects.filter(user=self.user)


class ExpenseForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="New Category (Optional)",
        widget=forms.TextInput(attrs={"placeholder": "New category"}),
    )

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Expense title"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Amount in Euro"}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Add an optional description", "rows": 2}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Fetch predefined categories + categories created by the user
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(
                predefined=True
            ) | Category.objects.filter(user=self.user)

    def clean_new_category(self):
        category_name = self.cleaned_data.get("category")
        new_category_name = self.cleaned_data.get("new_category")
        new_category_name = new_category_name.title()

        # Check for duplicate categories
        if category_name == None:
            if new_category_name == "":
                raise forms.ValidationError(
                    "Either choose predefined catagory or create one."
                )
            else:
                if (
                    Category.objects.filter(
                        name=new_category_name, predefined=True
                    ).exists()
                ) or (
                    Category.objects.filter(
                        name=new_category_name, user=self.user
                    ).exists()
                ):
                    raise forms.ValidationError(
                        "This category already exists for your account."
                    )
                else:
                    return new_category_name
