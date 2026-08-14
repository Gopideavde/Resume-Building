from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from templates_app.models import ResumeTemplate, TemplateCategory
from payments.models import PaymentTransaction, PremiumAccess
from unittest.mock import patch
import razorpay

class PaymentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password123')
        self.category = TemplateCategory.objects.create(name='Cat', slug='cat')
        self.template = ResumeTemplate.objects.create(name='Premium', slug='premium', category=self.category, is_premium=True, price=199.0)

    @patch('razorpay.Client')
    def test_create_order(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.order.create.return_value = {'id': 'order_test123'}

        self.client.login(username='test@example.com', password='password123')
        response = self.client.get(reverse('create_order', args=[self.template.id]))
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(PaymentTransaction.objects.filter(razorpay_order_id='order_test123').exists())

    @patch('razorpay.Utility.verify_payment_signature')
    def test_payment_verify_success(self, mock_verify):
        mock_verify.return_value = True 
        
        transaction = PaymentTransaction.objects.create(
            user=self.user, template=self.template, amount=199.0, currency='INR', razorpay_order_id='order_test123', status='PENDING'
        )

        self.client.login(username='test@example.com', password='password123')
        response = self.client.post(reverse('payment_verify'), {
            'razorpay_payment_id': 'pay_test123',
            'razorpay_order_id': 'order_test123',
            'razorpay_signature': 'sig_test123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment Successful')
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'SUCCESS')
        self.assertTrue(PremiumAccess.objects.filter(user=self.user, template=self.template).exists())

    @patch('razorpay.Utility.verify_payment_signature')
    def test_payment_verify_failure(self, mock_verify):
        mock_verify.side_effect = razorpay.errors.SignatureVerificationError("Invalid sig")
        
        transaction = PaymentTransaction.objects.create(
            user=self.user, template=self.template, amount=199.0, currency='INR', razorpay_order_id='order_test123', status='PENDING'
        )

        self.client.login(username='test@example.com', password='password123')
        response = self.client.post(reverse('payment_verify'), {
            'razorpay_payment_id': 'pay_test123',
            'razorpay_order_id': 'order_test123',
            'razorpay_signature': 'bad_sig'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment Failed')
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'FAILED')
        self.assertFalse(PremiumAccess.objects.filter(user=self.user, template=self.template).exists())
