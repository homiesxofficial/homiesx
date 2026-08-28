from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("platform_core", "0002_studentprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="maintenance_message",
            field=models.CharField(default="We are making a few improvements. Please check back soon.", max_length=240),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="maintenance_mode",
            field=models.BooleanField(default=False),
        ),
    ]