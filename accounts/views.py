from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth import login
from django.views import View
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from rest_framework.authtoken.models import Token


# Create your views here.
@login_required
def generate_api(request):
    usr = request.user
    token = Token.objects.get(user=usr)
    if token:
        return render(request, "accounts/api.html", {"token": token})
    else:
        if request.method == "POST":
            token = Token.objects.create(user=usr)
            token = Token.objects.get(user=usr)
            return render(request, "accounts/api.html", {"token": token})
        else:
            return render(request, "accounts/api.html")


class RegistrationView(View):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect to the homepage or another page
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect to the homepage or another page
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect to the homepage or another page
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("password_change_done")


@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect(
            "home"
        )  # Redirect to the homepage or any other page after deletion
    return render(request, "accounts/delete_user.html")
