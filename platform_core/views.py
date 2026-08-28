from django.shortcuts import render
from django.db.models import Q
from .models import Event, Opportunity, Project, Resource, SiteSettings
from .recommendations import campus_guide


def public_page(request, template, context=None):
    site_settings = SiteSettings.objects.filter(is_published=True).first()
    if site_settings and site_settings.maintenance_mode:
        return render(request, "platform_core/maintenance.html", {"settings": site_settings})
    return render(request, template, {**(context or {}), "settings": site_settings})


def home(request):
    settings = SiteSettings.objects.filter(is_published=True).first()
    year = request.GET.get("year", "all")
    year_filter = Q(study_year=year) | Q(study_year="all") if year in {"fy", "sy", "ty"} else Q()
    return public_page(request, "platform_core/home.html", {"settings": settings, "year": year, "featured_resources": Resource.objects.filter(is_published=True).filter(year_filter)[:3], "upcoming_events": Event.objects.filter(is_published=True).filter(year_filter).order_by("starts_at")[:3], "open_opportunities": Opportunity.objects.filter(is_published=True).filter(year_filter).order_by("deadline")[:3], "open_projects": Project.objects.filter(is_published=True).filter(year_filter).filter(status="open")[:3]})


def guide(request):
    query = request.GET.get("q", "").strip()
    year = request.GET.get("year", "all")
    return public_page(request, "platform_core/guide.html", {"query": query, "year": year, "matches": campus_guide(query, year) if query else []})


def resources(request):
    return public_listing(request, Resource, "Resources", "resource")


def events(request):
    return public_listing(request, Event, "Events", "event", "starts_at")


def opportunities(request):
    return public_listing(request, Opportunity, "Opportunities", "opportunity", "deadline")


def projects(request):
    return public_listing(request, Project, "Projects", "project")


def public_listing(request, model, title, kind, ordering=None):
    query = request.GET.get("q", "").strip()
    year = request.GET.get("year", "all")
    items = model.objects.filter(is_published=True)
    if year in {"fy", "sy", "ty"}:
        items = items.filter(Q(study_year=year) | Q(study_year="all"))
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if ordering:
        items = items.order_by(ordering)
    return public_page(request, "platform_core/list.html", {"title": title, "items": items, "kind": kind, "query": query, "year": year})


def about(request):
    return public_page(request, "platform_core/about.html")


def contact(request):
    return public_page(request, "platform_core/contact.html")
