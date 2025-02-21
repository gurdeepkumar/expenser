from django.shortcuts import render


# Create your views here.
def home(request):
    # return HttpResponse("Welcome to Expenser!")
    return render(request, "core/home.html")
