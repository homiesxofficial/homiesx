from django.contrib import admin
from .models import Event, Opportunity, Project, Resource, SiteSettings, StudentLoginHistory, StudentProfile

admin.site.site_header = "HOMIESX Control Panel"
admin.site.site_title = "HOMIESX Admin"
admin.site.index_title = "Manage HOMIESX platform content"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (("Brand", {"fields": ("brand_name", "tagline")}), ("Hero", {"fields": ("hero_eyebrow", "hero_heading", "hero_description", "primary_cta_label", "primary_cta_url")}), ("About page", {"fields": ("about_heading", "about_description")}), ("Contact details", {"fields": ("contact_email", "contact_phone", "contact_address")}), ("Social links", {"fields": ("instagram_url", "linkedin_url")}), ("Maintenance", {"fields": ("maintenance_mode", "maintenance_message")}), ("Footer", {"fields": ("footer_text",)}), ("Publishing", {"fields": ("is_published",)}))

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "study_year", "subject", "semester", "is_published", "created_at")
    list_filter = ("resource_type", "is_published", "semester")
    search_fields = ("title", "description", "subject")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "study_year", "starts_at", "venue", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "description", "venue")


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "opportunity_type", "study_year", "organisation", "deadline", "is_published")
    list_filter = ("opportunity_type", "is_published")
    search_fields = ("title", "description", "organisation")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "study_year", "team_size", "team_capacity", "is_published")
    list_filter = ("status", "is_published")
    search_fields = ("title", "description", "skills")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("title", "user_email", "mobile_number", "course", "campus", "is_verified", "is_active")
    list_filter = ("is_verified", "is_active", "course", "campus")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "mobile_number", "course", "campus")

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email


@admin.register(StudentLoginHistory)
class StudentLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "method", "successful", "created_at", "ip_address")
    list_filter = ("method", "successful", "created_at")
    search_fields = ("name", "email", "user__username", "ip_address")
    readonly_fields = [field.name for field in StudentLoginHistory._meta.fields]
