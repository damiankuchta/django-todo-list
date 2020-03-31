from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CreateUserForm


def check_if_logged(request):
    if request.user.is_authenticated:
        return redirect(reverse("display-lists"))
    else:
        return redirect(reverse("login"), {"title": "Login"})


def create_account(request):
    if request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('display-lists')
    else:
        form = CreateUserForm()
    return render(request, "AuthUser/create_account.html", {"form": form,
                                                            "title": "Create account"})

def logout(request):
    auth_logout(request)
    return redirect(reverse("login"))