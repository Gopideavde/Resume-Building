from django.shortcuts import render

def home_view(request):
    from templates_app.models import ResumeTemplate
    # Fetch templates for the showcase
    templates = ResumeTemplate.objects.filter(is_active=True)[:6]
    return render(request, 'core/home.html', {'templates': templates})

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    return render(request, 'core/contact.html')

def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')

def terms_view(request):
    return render(request, 'core/terms.html')
