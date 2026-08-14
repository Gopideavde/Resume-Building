from django.contrib import admin
from .models import Plan, PaymentTransaction, PremiumAccess

admin.site.register(Plan)
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'amount', 'status', 'razorpay_order_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('user', 'template', 'amount', 'currency', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'status', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(PremiumAccess)
class PremiumAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'granted_at')
    list_filter = ('granted_at',)
    search_fields = ('user__email', 'template__name')
    readonly_fields = ('user', 'template', 'payment', 'granted_at')
    date_hierarchy = 'granted_at'
