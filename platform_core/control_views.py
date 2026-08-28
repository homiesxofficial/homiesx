from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.utils import timezone

from .models import Event, Opportunity, Project, Resource, SiteSettings, StudentLoginHistory, StudentProfile


STAFF_REQUIRED = user_passes_test(
    lambda user: user.is_active and user.is_staff,
    login_url="control_login",
)

SECTIONS = {
    "students": {"model": StudentProfile, "label": "Students", "description": "Student accounts, contact details, and verification status.", "search_fields": ("user__username", "user__first_name", "user__last_name", "user__email", "course", "campus")},
    "resources": {"model": Resource, "label": "Resources", "description": "Academic material and useful student links.", "search_fields": ("title", "description", "subject", "semester")},
    "events": {"model": Event, "label": "Events", "description": "Campus events and registration details.", "search_fields": ("title", "description", "venue", "category")},
    "opportunities": {"model": Opportunity, "label": "Opportunities", "description": "Internships, scholarships, hackathons, and competitions.", "search_fields": ("title", "description", "organisation", "opportunity_type")},
    "projects": {"model": Project, "label": "Projects", "description": "Student project listings and team capacity.", "search_fields": ("title", "description", "skills", "status")},
}


def control_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("control_dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.POST.get("next") or "control_dashboard")
    return render(request, "platform_core/control/login.html", {"form": form, "next": request.GET.get("next", "")})


def control_logout(request):
    logout(request)
    return redirect("control_login")


@STAFF_REQUIRED
def control_dashboard(request):
    stats = [
        ("Students", StudentProfile.objects.count(), "students", "Member directory"),
        ("Resources", Resource.objects.count(), "resources", "Academic library"),
        ("Events", Event.objects.count(), "events", "Campus calendar"),
        ("Opportunities", Opportunity.objects.count(), "opportunities", "Student growth"),
        ("Projects", Project.objects.count(), "projects", "Collaboration space"),
    ]
    recent_items = []
    for section, model in (("students", StudentProfile), ("resources", Resource), ("events", Event), ("opportunities", Opportunity), ("projects", Project)):
        recent_items.extend({"item": item, "section": section} for item in model.objects.all()[:3])
    recent_items.sort(key=lambda entry: entry["item"].created_at, reverse=True)
    return render(request, "platform_core/control/dashboard.html", {
        "stats": stats,
        "site_settings": SiteSettings.objects.first(),
        "recent_items": recent_items[:8],
        "today": timezone.localdate(),
    })


def get_section(section):
    try:
        return SECTIONS[section]
    except KeyError as error:
        raise Http404("Unknown content section") from error


@STAFF_REQUIRED
def control_list(request, section):
    config = get_section(section)
    items = config["model"].objects.all()
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected")
        action = request.POST.get("bulk_action")
        status_field = "is_active" if section == "students" else "is_published"
        if selected_ids and action in {"enable", "disable"}:
            config["model"].objects.filter(pk__in=selected_ids).update(**{status_field: action == "enable"})
            return redirect("control_list", section=section)
    query = request.GET.get("q", "").strip()
    if query:
        filters = Q()
        for field in config["search_fields"]:
            filters |= Q(**{f"{field}__icontains": query})
        items = items.filter(filters)
    status = request.GET.get("status", "all")
    status_field = "is_active" if section == "students" else "is_published"
    if status == "published":
        items = items.filter(**{status_field: True})
    elif status == "draft":
        items = items.filter(**{status_field: False})
    page = Paginator(items, 10).get_page(request.GET.get("page"))
    return render(request, "platform_core/control/list.html", {"section": section, "config": config, "items": page, "query": query, "status": status, "status_field": status_field})


@STAFF_REQUIRED
def control_create(request, section):
    config = get_section(section)
    form_class = modelform_factory(config["model"], fields="__all__")
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("control_list", section=section)
    return render(request, "platform_core/control/form.html", {"form": form, "section": section, "config": config, "action": "Create"})


@STAFF_REQUIRED
def control_edit(request, section, pk):
    config = get_section(section)
    item = get_object_or_404(config["model"], pk=pk)
    form_class = modelform_factory(config["model"], fields="__all__")
    form = form_class(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("control_list", section=section)
    return render(request, "platform_core/control/form.html", {"form": form, "section": section, "config": config, "item": item, "action": "Save"})


@STAFF_REQUIRED
def control_delete(request, section, pk):
    config = get_section(section)
    item = get_object_or_404(config["model"], pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("control_list", section=section)
    return render(request, "platform_core/control/delete.html", {"section": section, "config": config, "item": item})


@STAFF_REQUIRED
def control_settings(request):
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    form_class = modelform_factory(SiteSettings, fields="__all__")
    form = form_class(request.POST or None, instance=settings)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("control_dashboard")
    return render(request, "platform_core/control/form.html", {"form": form, "config": {"label": "Site settings", "description": "Control the public home-page copy and call to action."}, "action": "Save"})


@STAFF_REQUIRED
def control_login_history(request):
    query = request.GET.get("q", "").strip()
    history = StudentLoginHistory.objects.all()
    if query:
        history = history.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(user__username__icontains=query))
    return render(request, "platform_core/control/login_history.html", {"history": history[:100], "query": query, "section": "login_history"})
