from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from platform_core.models import Event, Opportunity, Project, Resource, SiteSettings


class Command(BaseCommand):
    help = "Create safe, clearly identifiable demo content for local HOMIESX development."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "brand_name": "GHRCEMP Hub",
                "tagline": "Connect. Learn. Create. Grow at Wagholi.",
                "hero_eyebrow": "GH Raisoni College · Pune-Wagholi",
                "hero_heading": "Your next move starts here.",
                "hero_description": "A focused student hub for FY, SY, and TY learners to find resources, events, opportunities, and project teammates.",
                "primary_cta_label": "Explore resources",
                "primary_cta_url": "/resources/",
            },
        )
        Resource.objects.get_or_create(
            title="Demo: Data Structures practice set",
            defaults={"description": "Sample academic resource for local development only.", "resource_type": "pdf", "subject": "Data Structures", "semester": "Semester 3"},
        )
        Event.objects.get_or_create(
            title="Demo: Build for Campus",
            defaults={"description": "Sample event for local development only.", "category": "hackathon", "starts_at": timezone.now() + timedelta(days=7), "venue": "Demo venue"},
        )
        Opportunity.objects.get_or_create(
            title="Demo: Frontend internship program",
            defaults={"description": "Sample opportunity for local development only.", "opportunity_type": "internship", "organisation": "Demo organisation", "deadline": timezone.localdate() + timedelta(days=14)},
        )
        Project.objects.get_or_create(
            title="Demo: Campus Companion App",
            defaults={"description": "Sample student project for local development only.", "status": "open", "skills": "UI/UX, JavaScript, Django", "team_size": 2, "team_capacity": 4},
        )
        self.stdout.write(self.style.SUCCESS("Demo HOMIESX content created or already present."))
