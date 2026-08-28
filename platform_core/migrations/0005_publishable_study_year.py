from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("platform_core", "0004_sitesettings_site_details")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="study_year",
            field=models.CharField(choices=[("all", "All years"), ("fy", "First year (FY)"), ("sy", "Second year (SY)"), ("ty", "Third year (TY)")], default="all", max_length=3),
        ),
        migrations.AddField(
            model_name="opportunity",
            name="study_year",
            field=models.CharField(choices=[("all", "All years"), ("fy", "First year (FY)"), ("sy", "Second year (SY)"), ("ty", "Third year (TY)")], default="all", max_length=3),
        ),
        migrations.AddField(
            model_name="project",
            name="study_year",
            field=models.CharField(choices=[("all", "All years"), ("fy", "First year (FY)"), ("sy", "Second year (SY)"), ("ty", "Third year (TY)")], default="all", max_length=3),
        ),
        migrations.AddField(
            model_name="resource",
            name="study_year",
            field=models.CharField(choices=[("all", "All years"), ("fy", "First year (FY)"), ("sy", "Second year (SY)"), ("ty", "Third year (TY)")], default="all", max_length=3),
        ),
    ]