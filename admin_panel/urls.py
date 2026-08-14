from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('payments/', views.admin_payments, name='admin_payments'),
    path('templates/', views.admin_templates, name='admin_templates'),
    path('templates/<uuid:template_id>/toggle/', views.admin_template_toggle, name='admin_template_toggle'),
    path('audit-logs/', views.admin_audit_logs, name='admin_audit_logs'),
]
