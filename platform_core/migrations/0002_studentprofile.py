from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("platform_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mobile_number", models.CharField(blank=True, max_length=20)),
                ("course", models.CharField(blank=True, max_length=120)),
                ("year_of_study", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("campus", models.CharField(blank=True, max_length=150)),
                ("bio", models.TextField(blank=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="student_profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "student profile", "verbose_name_plural": "student profiles"},
        ),
    ]
