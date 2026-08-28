from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("platform_core", "0003_sitesettings_maintenance")]

    operations = [
        migrations.AddField(model_name="sitesettings", name="about_description", field=models.TextField(default="HOMIESX brings students, knowledge, opportunities, and collaborators into one focused ecosystem.")),
        migrations.AddField(model_name="sitesettings", name="about_heading", field=models.CharField(default="A better way to move forward together.", max_length=180)),
        migrations.AddField(model_name="sitesettings", name="contact_address", field=models.CharField(blank=True, max_length=240)),
        migrations.AddField(model_name="sitesettings", name="contact_email", field=models.EmailField(default="hello@homiesx.com", max_length=254)),
        migrations.AddField(model_name="sitesettings", name="contact_phone", field=models.CharField(blank=True, max_length=40)),
        migrations.AddField(model_name="sitesettings", name="footer_text", field=models.CharField(default="Built for student momentum.", max_length=180)),
        migrations.AddField(model_name="sitesettings", name="instagram_url", field=models.URLField(blank=True)),
        migrations.AddField(model_name="sitesettings", name="linkedin_url", field=models.URLField(blank=True)),
    ]