from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from templates_app.models import ResumeTemplate, TemplateCategory
from resumes.models import Resume

class TemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password123', first_name='Test', last_name='User')
        self.category = TemplateCategory.objects.create(name='Test Category', slug='test-category')
        
        self.free_template = ResumeTemplate.objects.create(
            name='Free Template', slug='free-template', category=self.category, is_premium=False
        )
        self.premium_template = ResumeTemplate.objects.create(
            name='Premium Template', slug='premium-template', category=self.category, is_premium=True, price=199.00
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

    def test_use_free_template(self):
        self.client.login(username='test@example.com', password='password123')
        response = self.client.get(reverse('use_template', args=[self.free_template.id]) + f"?resume_id={self.resume.id}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/resumes/', response.url)
        self.resume.refresh_from_db()
        self.assertEqual(self.resume.template, self.free_template)

    def test_use_premium_template_without_access(self):
        self.client.login(username='test@example.com', password='password123')
        response = self.client.get(reverse('use_template', args=[self.premium_template.id]) + f"?resume_id={self.resume.id}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/payments/order/', response.url)
