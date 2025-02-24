from django import forms
from .models import Expense, Category


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
