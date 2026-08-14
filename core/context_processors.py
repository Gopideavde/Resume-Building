from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings(
            site_name="ResumePro",
            site_tagline="Build a Professional Resume That Gets Noticed",
            primary_color="#4f46e5",
            secondary_color="#334155",
            footer_text="© 2026 ResumePro. All rights reserved."
        )
    return {'site_settings': settings}
