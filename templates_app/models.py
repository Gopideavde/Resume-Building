from django.db import models
import uuid

class TemplateCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ResumeTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(TemplateCategory, on_delete=models.SET_NULL, null=True, related_name='templates')
    preview_image = models.ImageField(upload_to='template_previews/')
    html_identifier = models.CharField(max_length=100, help_text="e.g. 'modern-blue', maps to the template HTML file")
    description = models.TextField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price if premium")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
