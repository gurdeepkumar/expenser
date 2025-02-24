from django import forms
from .models import Expense, Category


class FilterForm(forms.Form):
    from django import forms


class FilterForm(forms.Form):

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
    category = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Category"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Fetch predefined categories + categories created by the user
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(
                predefined=True
            ) | Category.objects.filter(user=self.user)


class ExpenseForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a new category (optional)"}
        ),
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
