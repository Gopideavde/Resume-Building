from django.contrib import admin
from .models import FAQ, Testimonial, ContactMessage, Notification, AuditLog, SiteSettings

admin.site.site_header = "ResumePro Platform Admin"
admin.site.site_title = "ResumePro Admin Portal"
admin.site.index_title = "Welcome to ResumePro Management"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'is_active', 'primary_color', 'secondary_color')
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('question', 'answer')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'review')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'action', 'object_type', 'ip_address', 'timestamp')
    list_filter = ('object_type', 'timestamp')
    search_fields = ('admin_user__email', 'action', 'object_id')
    readonly_fields = ('admin_user', 'action', 'object_id', 'object_type', 'ip_address', 'timestamp')
    date_hierarchy = 'timestamp'
