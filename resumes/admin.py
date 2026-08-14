from django.contrib import admin
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project, Certification, Language, Achievement, Reference

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    inlines = [EducationInline, ExperienceInline, SkillInline]
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__email')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

admin.site.register(PersonalInfo)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Certification)
admin.site.register(Language)
admin.site.register(Achievement)
admin.site.register(Reference)
