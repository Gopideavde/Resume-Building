from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, UserProfile

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

    def test_registration_success(self):
        response = self.client.post(self.register_url, {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_registration_duplicate_email(self):
        response = self.client.post(self.register_url, {
            'email': 'test@example.com',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Email is already in use')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password')

    def test_logout(self):
        self.client.login(username='test@example.com', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_unauthorized_access(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
