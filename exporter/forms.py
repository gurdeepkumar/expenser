from django import forms
from expenses.models import Category


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
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )
    to_date = forms.DateField(
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        required=False,
    )
    export_types = [
        ("pdf", "PDF"),
        ("excel", "Excel"),
        ("csv", "CSV"),
    ]

    export_as = forms.ChoiceField(
        choices=export_types,
        required=False,
        label="Export as:",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Fetch predefined categories + categories created by the user + sorting fields
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(
                predefined=True
            ) | Category.objects.filter(user=self.user)
