from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password2")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("index")
        return render(request, "accounts/register.html", {"form": form})    