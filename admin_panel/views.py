from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import User
from resumes.models import Resume
from templates_app.models import ResumeTemplate
from payments.models import PaymentTransaction
from core.models import AuditLog

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin, login_url='home')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_resumes = Resume.objects.count()
    total_templates = ResumeTemplate.objects.count()
    premium_templates = ResumeTemplate.objects.filter(is_premium=True).count()
    
    successful_payments = PaymentTransaction.objects.filter(status='SUCCESS').count()
    failed_payments = PaymentTransaction.objects.filter(status='FAILED').count()
    
    revenue = sum(p.amount for p in PaymentTransaction.objects.filter(status='SUCCESS'))
    
    context = {
        'total_users': total_users,
        'total_resumes': total_resumes,
        'total_templates': total_templates,
        'premium_templates': premium_templates,
        'free_templates': total_templates - premium_templates,
        'successful_payments': successful_payments,
        'failed_payments': failed_payments,
        'revenue': revenue,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@user_passes_test(is_admin, login_url='home')
def admin_payments(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    payments = PaymentTransaction.objects.all().order_by('-created_at')
    
    if query:
        payments = payments.filter(razorpay_order_id__icontains=query) | payments.filter(user__email__icontains=query)
    if status:
        payments = payments.filter(status=status)
        
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status': status
    }
    return render(request, 'admin_panel/payments.html', context)

@user_passes_test(is_admin, login_url='home')
def admin_templates(request):
    templates = ResumeTemplate.objects.all().order_by('-created_at')
    context = {'templates': templates}
    return render(request, 'admin_panel/templates.html', context)

@user_passes_test(is_admin, login_url='home')
def admin_template_toggle(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(ResumeTemplate, id=template_id)
        # Toggle premium status
        template.is_premium = not template.is_premium
        template.save()
        messages.success(request, f"Template {template.name} premium status updated to {template.is_premium}")
        
        AuditLog.objects.create(
            admin_user=request.user,
            action=f"Changed {template.name} premium status to {template.is_premium}",
            object_id=str(template.id),
            object_type="ResumeTemplate",
            ip_address=request.META.get('REMOTE_ADDR')
        )
    return redirect('admin_templates')

@user_passes_test(is_admin, login_url='home')
def admin_audit_logs(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'admin_panel/audit_logs.html', context)
