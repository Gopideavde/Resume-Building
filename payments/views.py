import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import PaymentTransaction, PremiumAccess
from templates_app.models import ResumeTemplate
from core.models import AuditLog
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def get_razorpay_client():
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    
    if not key_id or not key_secret or key_id == 'rzp_test_placeholder':
        return None, "Payment gateway is not properly configured. Please contact the administrator."
        
    return razorpay.Client(auth=(key_id, key_secret)), None

@login_required
def create_order(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True, is_premium=True)
    
    if request.user.premium_access.filter(template=template).exists():
        return redirect('use_template', template_id=template.id)
        
    amount = int(template.price * 100)
    currency = "INR"
    
    if amount <= 0:
        return HttpResponseBadRequest("Invalid template price.")
        
    client, error_msg = get_razorpay_client()
    if not client:
        messages.error(request, error_msg)
        return redirect('home')
        
    try:
        razorpay_order = client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    except razorpay.errors.BadRequestError:
        messages.error(request, "Payment gateway is not properly configured. Please contact the administrator.")
        return redirect('home')
    except Exception as e:
        messages.error(request, "Payment gateway is currently unavailable.")
        return redirect('home')
    
    transaction = PaymentTransaction.objects.create(
        user=request.user,
        template=template,
        amount=template.price,
        currency=currency,
        razorpay_order_id=razorpay_order['id'],
        status='PENDING'
    )
    
    AuditLog.objects.create(
        admin_user=request.user,
        action="Premium purchase initiated",
        object_id=str(template.id),
        object_type="ResumeTemplate",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    context = {
        'template': template,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'transaction': transaction
    }
    
    return render(request, 'payments/checkout.html', context)

@csrf_exempt
@login_required
def payment_verify(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        transaction = get_object_or_404(PaymentTransaction, razorpay_order_id=razorpay_order_id, user=request.user)
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        # Prevent replay attacks
        if transaction.status == 'SUCCESS':
            context = {'status': 'success', 'transaction': transaction}
            return render(request, 'payments/status.html', context)
            
        client, error_msg = get_razorpay_client()
        if not client:
            context = {'status': 'failed', 'transaction': transaction, 'error': error_msg}
            return render(request, 'payments/status.html', context)
        
        try:
            client.utility.verify_payment_signature(params_dict)
            transaction.status = 'SUCCESS'
            transaction.razorpay_payment_id = razorpay_payment_id
            transaction.razorpay_signature = razorpay_signature
            transaction.save()
            
            PremiumAccess.objects.create(
                user=transaction.user,
                template=transaction.template,
                payment=transaction
            )
            
            AuditLog.objects.create(
                admin_user=request.user,
                action="Payment verification successful, Premium access granted",
                object_id=str(transaction.id),
                object_type="PaymentTransaction",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            context = {'status': 'success', 'transaction': transaction}
            return render(request, 'payments/status.html', context)
            
        except razorpay.errors.SignatureVerificationError:
            transaction.status = 'FAILED'
            transaction.save()
            
            AuditLog.objects.create(
                admin_user=request.user,
                action="Payment verification failed",
                object_id=str(transaction.id),
                object_type="PaymentTransaction",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            context = {'status': 'failed', 'transaction': transaction}
            return render(request, 'payments/status.html', context)
    else:
        return HttpResponseBadRequest()
