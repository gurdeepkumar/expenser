from django.db import migrations


def create_predefined_categories(apps, schema_editor):
    Category = apps.get_model("expenses", "Category")
    predefined_categories = [
        "Food",
        "Transport",
        "Utilities",
        "Entertainment",
        "Health",
        "Education",
        "Others",
    ]

    for category_name in predefined_categories:
        Category.objects.get_or_create(name=category_name, predefined=True)


class Migration(migrations.Migration):

    dependencies = [
        (
            "expenses",
            "0001_initial",
        ),  # Replace with the name of the last migration
    ]

    operations = [
        migrations.RunPython(create_predefined_categories),
    ]
