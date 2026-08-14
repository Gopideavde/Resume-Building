from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project, Certification, Language, Achievement, Reference, Hobby
from .forms import ResumeForm, PersonalInfoForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, CertificationForm, LanguageForm, AchievementForm, ReferenceForm, HobbyForm
from django.contrib import messages

@login_required
def create_resume(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled Resume')
        resume = Resume.objects.create(user=request.user, title=title)
        PersonalInfo.objects.create(
            resume=resume, 
            email=request.user.email, 
            first_name=request.user.first_name, 
            last_name=request.user.last_name
        )
        messages.success(request, 'Resume created successfully.')
        return redirect('resume_builder', resume_id=resume.id)
    return redirect('dashboard')

@login_required
def resume_builder(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if not resume.template:
        return redirect('template_list')
        
    from templates_app.services import user_can_use_template
    if not user_can_use_template(request.user, resume.template):
        return redirect('create_order', template_id=resume.template.id)

    try:
        personal_info = resume.personal_info
    except PersonalInfo.DoesNotExist:
        personal_info = PersonalInfo.objects.create(resume=resume)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        section = request.POST.get('section')
        if section == 'personal_info':
            form = PersonalInfoForm(request.POST, request.FILES, instance=personal_info)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': form.errors})
        
        # Adding items to multiple records (Education, Experience, etc.)
        # This can be handled by creating generic handlers or separate endpoints
        
        return JsonResponse({'status': 'error', 'message': 'Unknown section'})

    context = {
        'resume': resume,
        'p_form': PersonalInfoForm(instance=personal_info),
        'e_form': EducationForm(),
        'ex_form': ExperienceForm(),
        's_form': SkillForm(),
        'pr_form': ProjectForm(),
        'c_form': CertificationForm(),
        'l_form': LanguageForm(),
        'a_form': AchievementForm(),
        'r_form': ReferenceForm(),
        'h_form': HobbyForm(),
    }
    return render(request, 'resumes/builder.html', context)

SECTION_MAP = {
    'education': (Education, EducationForm),
    'experience': (Experience, ExperienceForm),
    'projects': (Project, ProjectForm),
    'skills': (Skill, SkillForm),
    'certifications': (Certification, CertificationForm),
    'languages': (Language, LanguageForm),
    'achievements': (Achievement, AchievementForm),
    'hobbies': (Hobby, HobbyForm),
    'references': (Reference, ReferenceForm),
}

from django.views.decorators.http import require_POST
import json

@login_required
@require_POST
def add_resume_item(request, resume_id, section):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if section not in SECTION_MAP:
        return JsonResponse({'success': False, 'message': 'Invalid section'})
    
    ModelClass, FormClass = SECTION_MAP[section]
    form = FormClass(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.resume = resume
        item.save()
        
        # Serialize fields dynamically to pass back data
        data = {'id': item.id}
        for field in form.cleaned_data:
            val = getattr(item, field)
            data[field] = str(val) if val is not None else ''
            
        return JsonResponse({'success': True, 'message': f'{section.capitalize()} added successfully', 'data': data})
    return JsonResponse({'success': False, 'message': 'Please correct the errors', 'errors': form.errors})

@login_required
@require_POST
def update_resume_item(request, resume_id, section, item_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if section not in SECTION_MAP:
        return JsonResponse({'success': False, 'message': 'Invalid section'})
    
    ModelClass, FormClass = SECTION_MAP[section]
    item = get_object_or_404(ModelClass, id=item_id, resume=resume)
    
    form = FormClass(request.POST, instance=item)
    if form.is_valid():
        form.save()
        
        data = {'id': item.id}
        for field in form.cleaned_data:
            val = getattr(item, field)
            data[field] = str(val) if val is not None else ''
            
        return JsonResponse({'success': True, 'message': f'{section.capitalize()} updated successfully', 'data': data})
    return JsonResponse({'success': False, 'message': 'Please correct the errors', 'errors': form.errors})

@login_required
@require_POST
def delete_resume_item(request, resume_id, section, item_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if section not in SECTION_MAP:
        return JsonResponse({'success': False, 'message': 'Invalid section'})
    
    ModelClass, FormClass = SECTION_MAP[section]
    item = get_object_or_404(ModelClass, id=item_id, resume=resume)
    item.delete()
    return JsonResponse({'success': True, 'message': f'{section.capitalize()} deleted successfully'})

@login_required
def resume_delete(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted.')
    return redirect('dashboard')

from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def resume_download(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if not resume.template:
        return redirect('template_list')
        
    from templates_app.services import user_can_use_template
    if not user_can_use_template(request.user, resume.template):
        return redirect('create_order', template_id=resume.template.id)

    # In a full implementation, we'd use resume.template.html_identifier
    # For now, use the default template
    template_name = 'resumes/templates/default.html'
    
    context = {'resume': resume}
    html_string = render_to_string(template_name, context)
    
    # Generate PDF
    try:
        import weasyprint
        pdf = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Resume_{resume.title}.pdf"'
        return response
    except OSError:
        # Fallback if GTK is not installed on Windows
        return HttpResponse("WeasyPrint system dependencies (GTK3) are not installed on this server. Please see README.", status=500)
