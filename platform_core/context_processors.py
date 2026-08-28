from .models import SiteSettings


def site_settings(request):
    return {"site_settings": SiteSettings.objects.filter(is_published=True).first()}
