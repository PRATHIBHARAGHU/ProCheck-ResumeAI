from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('analyzer:dashboard')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Smart Resume Analyzer.")
            return redirect('analyzer:dashboard')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('analyzer:dashboard')
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('analyzer:dashboard')
        messages.error(request, "Invalid username or password.")
        return render(request, 'accounts/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')