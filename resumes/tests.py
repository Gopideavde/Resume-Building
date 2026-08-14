from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from resumes.models import Resume, PersonalInfo

class ResumeCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1@example.com', email='user1@example.com', password='password123', first_name='User', last_name='One')
        self.user2 = User.objects.create_user(username='user2@example.com', email='user2@example.com', password='password123', first_name='User', last_name='Two')
        
        self.resume1 = Resume.objects.create(user=self.user1, title='User 1 Resume')
        self.resume2 = Resume.objects.create(user=self.user2, title='User 2 Resume')

    def test_resume_creation(self):
        self.client.login(username='user1@example.com', password='password123')
        response = self.client.post(reverse('create_resume'), {'title': 'New Resume'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resume.objects.filter(user=self.user1, title='New Resume').exists())
        
        new_resume = Resume.objects.get(user=self.user1, title='New Resume')
        self.assertTrue(hasattr(new_resume, 'personal_info'))
        self.assertEqual(new_resume.personal_info.email, self.user1.email)

    def test_resume_ownership_boundary(self):
        self.client.login(username='user1@example.com', password='password123')
        
        response = self.client.get(reverse('resume_builder', args=[self.resume2.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('resume_delete', args=[self.resume2.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Resume.objects.filter(id=self.resume2.id).exists())

    def test_resume_delete_success(self):
        self.client.login(username='user1@example.com', password='password123')
        response = self.client.post(reverse('resume_delete', args=[self.resume1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Resume.objects.filter(id=self.resume1.id).exists())

    def test_resume_builder_ajax_save(self):
        self.client.login(username='user1@example.com', password='password123')
        try:
            pi = self.resume1.personal_info
        except PersonalInfo.DoesNotExist:
            pi = PersonalInfo.objects.create(resume=self.resume1, first_name='Old', last_name='Name', email='old@example.com')
        
        response = self.client.post(
            reverse('resume_builder', args=[self.resume1.id]),
            {
                'section': 'personal_info',
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.resume1.personal_info.refresh_from_db()
        self.assertEqual(self.resume1.personal_info.first_name, 'Updated')
