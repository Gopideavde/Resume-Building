from django.db import models
from accounts.models import User

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        
    def __str__(self):
        return self.question

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}"

class AuditLog(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255, blank=True, null=True)
    object_type = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.admin_user} - {self.action} at {self.timestamp}"

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="ResumePro")
    site_tagline = models.CharField(max_length=255, default="Build a Professional Resume That Gets Noticed", blank=True)
    site_logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True)
    primary_color = models.CharField(max_length=20, default="#4f46e5", help_text="e.g. #4f46e5 (Indigo)")
    secondary_color = models.CharField(max_length=20, default="#334155", help_text="e.g. #334155 (Slate)")
    footer_text = models.TextField(default="© 2026 ResumePro. All rights reserved.", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name
