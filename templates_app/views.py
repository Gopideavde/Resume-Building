from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResumeTemplate, TemplateCategory

def template_list(request):
    categories = TemplateCategory.objects.filter(is_active=True)
    templates = ResumeTemplate.objects.filter(is_active=True)
    
    cat_slug = request.GET.get('category')
    if cat_slug:
        templates = templates.filter(category__slug=cat_slug)
        
    context = {
        'categories': categories,
        'templates': templates,
        'current_cat': cat_slug
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
