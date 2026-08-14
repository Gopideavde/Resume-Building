from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from resumes.models import Resume

@login_required
def dashboard_view(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    from payments.models import PaymentTransaction
    payments = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'resumes': resumes,
        'payments': payments,
    }
    return render(request, 'dashboard/dashboard.html', context)
