# cookieapp/authenticate.py
from rest_framework_simplejwt.authentication import JWTAuthentication, InvalidToken
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(JWTAuthentication):
    enforce = True

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        if self.enforce:
            enforce_csrf(request)
        return self.get_user(validated_token), validated_token


class AuthenticationMiddleware(AuthenticationMiddleware, CustomAuthentication):
    enforce = False

    def process_request(self, request):
        if not request.user.is_authenticated:
            request.user = SimpleLazyObject(
                lambda: self.get_user_request(request))

    def get_user_request(self, request):
        try:
            auth = self.authenticate(request)
            if auth is None:
                user = AnonymousUser()
            else:
                user = auth[0]
        except InvalidToken:
            user = AnonymousUser()
        request._cached_user = user
        return user
