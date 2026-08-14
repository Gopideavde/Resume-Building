from django import forms
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project, Certification, Language, Achievement, Reference, Hobby

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['resume']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['resume', 'order']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['resume', 'order']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['resume', 'order']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['resume', 'order']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ['resume', 'order']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ['resume', 'order']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ['resume', 'order']

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        exclude = ['resume', 'order']

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        exclude = ['resume', 'order']
