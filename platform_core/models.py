from django.db import models
from django.contrib.auth.models import User


class SiteSettings(models.Model):
    """Singleton content that controls the public HOMIESX landing page."""
    brand_name = models.CharField(max_length=40, default="HOMIESX")
    tagline = models.CharField(max_length=120, default="Connect. Learn. Create. Grow.")
    hero_eyebrow = models.CharField(max_length=120, default="The student ecosystem, rethought")
    hero_heading = models.CharField(max_length=180, default="More ways to move forward.")
    hero_description = models.TextField(default="HOMIESX brings the right resources, opportunities, projects, and student communities into one focused place.")
    primary_cta_label = models.CharField(max_length=60, default="Explore HOMIESX")
    primary_cta_url = models.CharField(max_length=200, default="/resources/")
    is_published = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.CharField(max_length=240, default="We are making a few improvements. Please check back soon.")
    about_heading = models.CharField(max_length=180, default="A better way to move forward together.")
    about_description = models.TextField(default="HOMIESX brings students, knowledge, opportunities, and collaborators into one focused ecosystem.")
    contact_email = models.EmailField(default="hello@homiesx.com")
    contact_phone = models.CharField(max_length=40, blank=True)
    contact_address = models.CharField(max_length=240, blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    footer_text = models.CharField(max_length=180, default="Built for student momentum.")

    class Meta:
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Public site settings"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    mobile_number = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=120, blank=True)
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    campus = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "student profile"
        verbose_name_plural = "student profiles"

    @property
    def title(self):
        return self.user.get_full_name() or self.user.username

    @property
    def description(self):
        details = [self.user.email, self.mobile_number, self.course]
        return " · ".join(detail for detail in details if detail) or "No profile details added yet."

    @property
    def is_published(self):
        return self.is_active

    def __str__(self):
        return self.title


class StudentLoginHistory(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="login_history")
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    method = models.CharField(max_length=20)
    successful = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "student login history"
        verbose_name_plural = "student login history"

    def __str__(self):
        return f"{self.name or self.email or 'Unknown student'} · {self.method}"


class Publishable(models.Model):
    class StudyYear(models.TextChoices):
        ALL = "all", "All years"
        FY = "fy", "First year (FY)"
        SY = "sy", "Second year (SY)"
        TY = "ty", "Third year (TY)"

    title = models.CharField(max_length=180)
    description = models.TextField()
    study_year = models.CharField(max_length=3, choices=StudyYear.choices, default=StudyYear.ALL)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Resource(Publishable):
    class ResourceType(models.TextChoices):
        NOTES = "notes", "Notes"
        PDF = "pdf", "PDF"
        LINK = "link", "Useful link"
    resource_type = models.CharField(max_length=12, choices=ResourceType.choices, default=ResourceType.NOTES)
    subject = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Event(Publishable):
    class Category(models.TextChoices):
        HACKATHON = "hackathon", "Hackathon"
        WORKSHOP = "workshop", "Workshop"
        SEMINAR = "seminar", "Seminar"
        COMMUNITY = "community", "Community"
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.WORKSHOP)
    starts_at = models.DateTimeField()
    venue = models.CharField(max_length=150, blank=True)
    registration_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Opportunity(Publishable):
    class OpportunityType(models.TextChoices):
        INTERNSHIP = "internship", "Internship"
        HACKATHON = "hackathon", "Hackathon"
        SCHOLARSHIP = "scholarship", "Scholarship"
        COMPETITION = "competition", "Competition"
    opportunity_type = models.CharField(max_length=20, choices=OpportunityType.choices)
    organisation = models.CharField(max_length=150)
    deadline = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Project(Publishable):
    class Status(models.TextChoices):
        OPEN = "open", "Looking for teammates"
        ACTIVE = "active", "In progress"
        CLOSED = "closed", "Team full"
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.OPEN)
    skills = models.CharField(max_length=300, help_text="Comma-separated skills, e.g. Python, UI/UX")
    team_size = models.PositiveSmallIntegerField(default=1)
    team_capacity = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.title
