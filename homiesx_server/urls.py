from django.contrib import admin
from django.urls import path

from platform_core import auth_views, control_views, views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/login/", control_views.control_login, name="control_login"),
    path("admin/logout/", control_views.control_logout, name="control_logout"),
    path("admin/", control_views.control_dashboard, name="control_dashboard"),
    path("admin/settings/", control_views.control_settings, name="control_settings"),
    path("admin/login-history/", control_views.control_login_history, name="control_login_history"),
    path("admin/<str:section>/", control_views.control_list, name="control_list"),
    path("admin/<str:section>/new/", control_views.control_create, name="control_create"),
    path("admin/<str:section>/<int:pk>/edit/", control_views.control_edit, name="control_edit"),
    path("admin/<str:section>/<int:pk>/delete/", control_views.control_delete, name="control_delete"),
    path("", views.home, name="home"),
    path("resources/", views.resources, name="resources"),
    path("events/", views.events, name="events"),
    path("opportunities/", views.opportunities, name="opportunities"),
    path("projects/", views.projects, name="projects"),
    path("guide/", views.guide, name="guide"),
    path("student/login/", auth_views.student_login, name="student_login"),
    path("student/signup/", auth_views.student_signup, name="student_signup"),
    path("student/logout/", auth_views.student_logout, name="student_logout"),
    path("student/dashboard/", auth_views.student_dashboard, name="student_dashboard"),
    path("student/oauth/<str:provider>/", lambda request, provider: auth_views.social_login(request, provider) if provider in {"google", "github"} else views.home(request), name="social_login"),
    path("student/oauth/<str:provider>/callback/", lambda request, provider: auth_views.social_callback(request, provider) if provider in {"google", "github"} else views.home(request), name="social_callback"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
