from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def home(request):
    # return HttpResponse("Welcome to Expenser!")
    return render(request, "core/home.html")
