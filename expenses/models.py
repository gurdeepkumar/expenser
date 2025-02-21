from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Null for predefined categories
    predefined = models.BooleanField(
        default=False
    )  # True for predefined, False for user-defined

    class Meta:
        unique_together = ("name", "user")  # Prevent duplicate categories per user

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Associate expense with a user
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
