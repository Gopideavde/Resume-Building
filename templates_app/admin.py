from django.contrib import admin
from .models import TemplateCategory, ResumeTemplate

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_premium', 'price', 'is_active', 'created_at')
    list_filter = ('is_premium', 'is_active', 'category')
    search_fields = ('name', 'description')
    
@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name',)
