from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
import openpyxl
import csv
from expenses.models import Category, Expense
from django.shortcuts import render
from .forms import RefiningForm


def exporter(request):
    if request.method == "POST":
        form = RefiningForm(request.POST, user=request.user)
        filter_expenses = Expense.objects.filter(user=request.user)
        if form.is_valid():
            # Get filter values from request
            selected_categories_ids = request.POST.getlist(
                "category"
            )  # Get multiple selected categories
            min_amount = request.POST.get("min_amount")
            max_amount = request.POST.get("max_amount")
            start_date = request.POST.get("from_date")
            end_date = request.POST.get("to_date")
            export_as = request.POST.get("export_as")

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

            if export_as == "pdf":
                # Create the HttpResponse object with PDF content type
                response = HttpResponse(content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="expenses.pdf"'

                # Create PDF canvas
                p = canvas.Canvas(response, pagesize=letter)
                width, height = letter  # Standard letter size (8.5 x 11 inches)

                # Title
                p.setFont("Helvetica-Bold", 16)
                p.drawString(
                    50,
                    height - 40,
                    f"Expense Report: {start_date} to {end_date}",
                )

                # Table headers
                y_position = height - 80
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y_position, "Title")
                p.drawString(200, y_position, "Category")
                p.drawString(350, y_position, "Amount")
                p.drawString(450, y_position, "Date")

                y_position -= 20  # Move down for data

                # Loop through expenses and add them to the PDF
                p.setFont("Helvetica", 10)
                for expense in filter_expenses:
                    if y_position < 50:  # Check if we need a new page
                        p.showPage()
                        p.setFont("Helvetica", 10)
                        y_position = height - 50

                    p.drawString(
                        50, y_position, expense.title[:20]
                    )  # Truncate long titles
                    p.drawString(200, y_position, expense.category.name)
                    p.drawString(350, y_position, f"€{expense.amount:.2f}")
                    p.drawString(450, y_position, expense.date.strftime("%Y-%m-%d"))
                    y_position -= 20  # Move to the next row

                # Save the PDF and return response
                p.showPage()
                p.save()
                return response
            elif export_as == "excel":
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Expenses Report"

                # Define headers
                headers = ["Title", "Category", "Amount", "Date"]
                ws.append(headers)

                # Add expense data to the Excel sheet
                for expense in filter_expenses:
                    ws.append(
                        [
                            expense.title,
                            expense.category.name,
                            expense.amount,
                            expense.date.strftime("%Y-%m-%d"),
                        ]
                    )

                # Create HTTP response with Excel content type
                response = HttpResponse(
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'

                # Save workbook to response
                wb.save(response)
                messages.success(
                    request, "Your excel sheet has been downloaded successfully! 😊"
                )
                return response
            elif export_as == "csv":
                # Create HTTP response with CSV content type
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = 'attachment; filename="expenses.csv"'

                # Create CSV writer
                writer = csv.writer(response)

                # Write header row
                writer.writerow(["Title", "Category", "Amount", "Date"])

                # Write expense data to CSV
                for expense in filter_expenses:
                    writer.writerow(
                        [
                            expense.title,
                            expense.category.name,
                            expense.amount,
                            expense.date.strftime("%Y-%m-%d"),
                        ]
                    )
                messages.success(
                    request, "Your CSV has been downloaded successfully! 😊"
                )
                return response

        return render(
            request,
            "exporter/exporter.html",
            {
                "filter_form": form,
            },
        )
    else:
        form = RefiningForm(user=request.user)
        return render(
            request,
            "exporter/exporter.html",
            {
                "filter_form": form,
            },
        )
