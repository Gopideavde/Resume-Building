from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResumeTemplate, TemplateCategory

def template_list(request):
    categories = TemplateCategory.objects.filter(is_active=True)
    templates = ResumeTemplate.objects.filter(is_active=True)
    
    cat_slug = request.GET.get('category')
    if cat_slug:
        templates = templates.filter(category__slug=cat_slug)
        
    type_filter = request.GET.get('type')
    if type_filter == 'free':
        templates = templates.filter(is_premium=False)
    elif type_filter == 'premium':
        templates = templates.filter(is_premium=True)
        
    search_query = request.GET.get('q')
    if search_query:
        templates = templates.filter(name__icontains=search_query)
        
    context = {
        'categories': categories,
        'templates': templates,
        'current_cat': cat_slug,
        'current_type': type_filter,
        'search_query': search_query,
    }
    return render(request, 'templates_app/list.html', context)

@login_required
def use_template(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    resume_id = request.GET.get('resume_id')
    
    from .services import user_can_use_template
    
    if not user_can_use_template(request.user, template):
        return redirect('create_order', template_id=template.id)
            
    from resumes.models import Resume
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        resume.template = template
        resume.save()
        return redirect('resume_builder', resume_id=resume.id)
    else:
        resume = Resume.objects.create(user=request.user, title=f"Resume with {template.name}", template=template)
        return redirect('resume_builder', resume_id=resume.id)

def template_demo(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    identifier = template.html_identifier if template.html_identifier else 'default'
    template_name = f'resumes/templates/{identifier}.html'
    
    # Create a dummy resume object to pass to the template
    class DummyResume:
        def __init__(self, title):
            self.title = title
            self.personal_info = type('DummyPI', (), {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '+1 234 567 8900',
                'location': 'New York, USA',
                'linkedin': 'linkedin.com/in/johndoe',
                'professional_summary': 'Results-driven Senior Software Engineer with over 8 years of experience in designing and developing scalable web applications. Proven expertise in Python, Django, and modern frontend frameworks. Adept at leading cross-functional teams to deliver high-quality software solutions.'
            })()
            
            class DummyExp:
                job_title = 'Senior Software Engineer'
                company = 'Tech Solutions Inc.'
                location = 'San Francisco, CA'
                start_date = '2019-03-01'
                end_date = 'Present'
                description = 'Led the development of a microservices architecture.\nMentored junior developers and improved code quality by 40%.\nImplemented CI/CD pipelines.'
            self.experiences = type('DummyExpManager', (), {'all': lambda: [DummyExp()]})()
            
            class DummyEdu:
                degree = 'B.S. in Computer Science'
                school = 'University of Technology'
                location = 'Boston, MA'
                start_date = '2011-09-01'
                end_date = '2015-05-01'
                description = 'Graduated with Honors. Vice President of the Computer Science Society.'
            self.educations = type('DummyEduManager', (), {'all': lambda: [DummyEdu()]})()
            
            class DummySkill:
                def __init__(self, n, l):
                    self.name = n
                    self.level = l
            self.skills = type('DummySkillManager', (), {'all': lambda: [DummySkill('Python', 'Expert'), DummySkill('Django', 'Expert'), DummySkill('JavaScript', 'Advanced')]})()
            
            # Empty placeholders for other relations to prevent errors
            self.projects = type('EmptyManager', (), {'all': lambda: []})()
            self.certifications = type('EmptyManager', (), {'all': lambda: []})()
            self.languages = type('EmptyManager', (), {'all': lambda: []})()
            self.achievements = type('EmptyManager', (), {'all': lambda: []})()
            self.hobbies = type('EmptyManager', (), {'all': lambda: []})()
            self.references = type('EmptyManager', (), {'all': lambda: []})()

    dummy_resume = DummyResume("Demo Resume")
    
    if request.GET.get('raw'):
        return render(request, template_name, {'resume': dummy_resume, 'is_demo': True})
    else:
        return render(request, 'templates_app/demo.html', {'template': template})

