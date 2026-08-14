from django.contrib import admin
from .models import TemplateCategory, ResumeTemplate
from django.utils.html import format_html

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('admin_preview', 'name', 'category', 'is_premium', 'price', 'is_active', 'created_at')
    list_filter = ('is_premium', 'is_active', 'category')
    search_fields = ('name', 'description')
    list_editable = ('is_premium', 'price', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

    def admin_preview(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px;" />', obj.preview_image.url)
        return "-"
    admin_preview.short_description = 'Preview'
    
@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name',)
