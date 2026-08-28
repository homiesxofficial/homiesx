# Generated manually because Python/Django is not available in this workspace.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.CharField(choices=[("hackathon", "Hackathon"), ("workshop", "Workshop"), ("seminar", "Seminar"), ("community", "Community")], default="workshop", max_length=20)),
                ("starts_at", models.DateTimeField()),
                ("venue", models.CharField(blank=True, max_length=150)),
                ("registration_url", models.URLField(blank=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("opportunity_type", models.CharField(choices=[("internship", "Internship"), ("hackathon", "Hackathon"), ("scholarship", "Scholarship"), ("competition", "Competition")], max_length=20)),
                ("organisation", models.CharField(max_length=150)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("application_url", models.URLField(blank=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("open", "Looking for teammates"), ("active", "In progress"), ("closed", "Team full")], default="open", max_length=12)),
                ("skills", models.CharField(help_text="Comma-separated skills, e.g. Python, UI/UX", max_length=300)),
                ("team_size", models.PositiveSmallIntegerField(default=1)),
                ("team_capacity", models.PositiveSmallIntegerField(default=4)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("resource_type", models.CharField(choices=[("notes", "Notes"), ("pdf", "PDF"), ("link", "Useful link")], default="notes", max_length=12)),
                ("subject", models.CharField(blank=True, max_length=100)),
                ("semester", models.CharField(blank=True, max_length=50)),
                ("url", models.URLField(blank=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("brand_name", models.CharField(default="HOMIESX", max_length=40)),
                ("tagline", models.CharField(default="Connect. Learn. Create. Grow.", max_length=120)),
                ("hero_eyebrow", models.CharField(default="The student ecosystem, rethought", max_length=120)),
                ("hero_heading", models.CharField(default="More ways to move forward.", max_length=180)),
                ("hero_description", models.TextField(default="HOMIESX brings the right resources, opportunities, projects, and student communities into one focused place.")),
                ("primary_cta_label", models.CharField(default="Explore HOMIESX", max_length=60)),
                ("primary_cta_url", models.CharField(default="/resources/", max_length=200)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={"verbose_name_plural": "site settings"},
        ),
    ]
