import json

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

# to be used for social authentication with python social auth
# from requests.exceptions import HTTPError
# from rest_framework import permissions, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view  # , permission_classes

# from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from social_django.utils import psa

# from .serializers import UserSerializer
# from .utils.social.oauth import get_access_token_from_code

# User = get_user_model()


from django.shortcuts import render

# Create your views here.


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"detail": "Logout Successful"})


@ensure_csrf_cookie
def login_set_cookie(request):
    """
    `login_view` requires that a csrf cookie be set.
    `getCsrfToken` in `auth.js` uses this cookie to
    make a request to `login_view`
    """
    return JsonResponse({"details": "CSRF cookie set"})


@require_POST
def login_view(request):
    """
    This function logs in the user and returns
    and HttpOnly cookie, the `sessionid` cookie
    """
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    if email is None or password is None:
        return JsonResponse(
            {"errors": {"__all__": "Please enter both username and password"}},
            status=400,
        )
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"detail": "Success"})
    return JsonResponse({"detail": "Invalid credentials"}, status=400)


@api_view(["POST", "DELETE"])
def request_api_token(request):
    user = request.user
    if request.method == "POST":
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    else:
        tokens = Token.objects.filter(user=user).delete()
        return Response({"detail": "All of your tokens have been deleted"})
