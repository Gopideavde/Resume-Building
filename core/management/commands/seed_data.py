from django.core.management.base import BaseCommand
from templates_app.models import TemplateCategory, ResumeTemplate
from payments.models import Plan
from core.models import FAQ, Testimonial

class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        cat1, _ = TemplateCategory.objects.get_or_create(name='Professional', slug='professional')
        cat2, _ = TemplateCategory.objects.get_or_create(name='Creative', slug='creative')
        cat3, _ = TemplateCategory.objects.get_or_create(name='ATS Friendly', slug='ats-friendly')

        ResumeTemplate.objects.get_or_create(
            slug='modern-blue',
            defaults={
                'name': 'Modern Blue',
                'category': cat1,
                'html_identifier': 'modern-blue',
                'description': 'A clean professional template with blue accents.',
                'is_premium': False
            }
        )
        ResumeTemplate.objects.get_or_create(
            slug='minimal-ats',
            defaults={
                'name': 'Minimal ATS',
                'category': cat3,
                'html_identifier': 'minimal-ats',
                'description': 'Highly optimized for ATS scanners. No columns.',
                'is_premium': False
            }
        )
        ResumeTemplate.objects.get_or_create(
            slug='corporate-premium',
            defaults={
                'name': 'Corporate Premium',
                'category': cat1,
                'html_identifier': 'corporate-premium',
                'description': 'A premium corporate template.',
                'is_premium': True,
                'price': 299.00
            }
        )

        FAQ.objects.get_or_create(
            question='Is the free plan really free?',
            defaults={'answer': 'Yes, you can use our free templates forever.', 'display_order': 1}
        )
        
        Testimonial.objects.get_or_create(
            name='John Doe',
            defaults={
                'designation': 'Software Engineer',
                'review': 'This resume builder helped me get my dream job!',
                'rating': 5
            }
        )

        Plan.objects.get_or_create(
            name='Premium Subscription',
            defaults={
                'price': 299.00,
                'duration_days': 30,
                'description': 'Unlock all premium templates for 30 days.'
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with demo data.'))
