from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.normal_user = User.objects.create_user(username='normal@example.com', email='normal@example.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com', password='password123')
        self.admin_url = reverse('admin_dashboard')

    def test_guest_cannot_access_admin(self):
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)

    def test_normal_user_cannot_access_admin(self):
        self.client.login(username='normal@example.com', password='password123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_admin(self):
        self.client.login(username='admin@example.com', password='password123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)
