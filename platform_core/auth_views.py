import json
import os
import secrets
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import StudentLoginHistory, StudentProfile


class StudentSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")


def record_login(request, method, user=None, email="", successful=False):
    StudentLoginHistory.objects.create(
        user=user,
        name=user.get_full_name() if user else "",
        email=email or (user.email if user else ""),
        method=method,
        successful=successful,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
    )


def student_login(request):
    form = None
    error = ""
    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=identifier, password=password)
        if user is None and "@" in identifier:
            account = User.objects.filter(email__iexact=identifier).first()
            user = authenticate(request, username=account.username, password=password) if account else None
        if user and user.is_active:
            record_login(request, "password", user=user, successful=True)
            login(request, user)
            return redirect(request.POST.get("next") or "student_dashboard")
        record_login(request, "password", email=identifier if "@" in identifier else "", successful=False)
        error = "The email or password is incorrect."
    return render(request, "platform_core/auth/login.html", {"form": form, "error": error, "next": request.GET.get("next", "")})


def student_signup(request):
    form = StudentSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        StudentProfile.objects.create(user=user, course=request.POST.get("course", ""), year_of_study=request.POST.get("year_of_study") or None, campus="GHRCEMP, Pune-Wagholi")
        login(request, user)
        return redirect("student_dashboard")
    return render(request, "platform_core/auth/signup.html", {"form": form})


def student_logout(request):
    logout(request)
    return redirect("student_login")


def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("student_login")
    profile = getattr(request.user, "student_profile", None)
    year_labels = {1: "FY", 2: "SY", 3: "TY"}
    return render(request, "platform_core/auth/dashboard.html", {"profile": profile, "year_label": year_labels.get(profile.year_of_study) if profile else "Student"})


def social_login(request, provider):
    client_id = os.environ.get(f"SOCIAL_AUTH_{provider.upper()}_CLIENT_ID")
    if not client_id:
        record_login(request, provider, successful=False)
        return render(request, "platform_core/auth/login.html", {"error": f"{provider.title()} login needs its client ID configured by the site administrator."})
    state = secrets.token_urlsafe(24)
    request.session[f"oauth_state_{provider}"] = state
    redirect_uri = request.build_absolute_uri(f"/student/oauth/{provider}/callback/")
    if provider == "google":
        params = {"client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code", "scope": "openid email profile", "state": state}
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    else:
        params = {"client_id": client_id, "redirect_uri": redirect_uri, "scope": "read:user user:email", "state": state}
        url = "https://github.com/login/oauth/authorize?" + urlencode(params)
    return redirect(url)


def social_callback(request, provider):
    state = request.GET.get("state")
    if not state or state != request.session.pop(f"oauth_state_{provider}", None):
        record_login(request, provider, successful=False)
        return render(request, "platform_core/auth/login.html", {"error": "Social login verification failed. Please try again."})
    code = request.GET.get("code")
    client_id = os.environ.get(f"SOCIAL_AUTH_{provider.upper()}_CLIENT_ID")
    client_secret = os.environ.get(f"SOCIAL_AUTH_{provider.upper()}_CLIENT_SECRET")
    if not code or not client_id or not client_secret:
        record_login(request, provider, successful=False)
        return render(request, "platform_core/auth/login.html", {"error": "Social login configuration is incomplete."})
    redirect_uri = request.build_absolute_uri(f"/student/oauth/{provider}/callback/")
    token_url = "https://oauth2.googleapis.com/token" if provider == "google" else "https://github.com/login/oauth/access_token"
    payload = urlencode({"client_id": client_id, "client_secret": client_secret, "code": code, "redirect_uri": redirect_uri}).encode()
    token_request = Request(token_url, data=payload, headers={"Accept": "application/json"})
    try:
        with urlopen(token_request, timeout=8) as response:
            token = json.loads(response.read())
        access_token = token.get("access_token")
        if not access_token:
            raise ValueError("No access token returned")
        user_url = "https://openidconnect.googleapis.com/v1/userinfo" if provider == "google" else "https://api.github.com/user"
        user_request = Request(user_url, headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"})
        with urlopen(user_request, timeout=8) as response:
            identity = json.loads(response.read())
    except (HTTPError, OSError, ValueError, json.JSONDecodeError):
        record_login(request, provider, successful=False)
        return render(request, "platform_core/auth/login.html", {"error": "Could not complete social login. Please try again."})
    email = identity.get("email")
    if not email:
        record_login(request, provider, successful=False)
        return render(request, "platform_core/auth/login.html", {"error": "Your provider did not share an email address."})
    user, created = User.objects.get_or_create(email=email, defaults={"username": f"student_{secrets.token_hex(5)}", "first_name": identity.get("name", "")})
    if created:
        user.set_unusable_password()
        user.save(update_fields=["password"])
        StudentProfile.objects.create(user=user, campus="GHRCEMP, Pune-Wagholi")
    login(request, user)
    record_login(request, provider, user=user, successful=True)
    return redirect("student_dashboard")
