from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, logout
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def login(response, user):
    data = get_tokens_for_user(user)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=data["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user: User = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                response = redirect("catalog")
                login(response, user)
                return response
        return render(request, 'users/login.html', {'form': form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            response = redirect("catalog")
            login(response, user)
            return response

        return render(request, 'users/register.html', {'form': form})
