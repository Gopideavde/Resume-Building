import os
import re

dir_path = "C:\\Users\\GOPI\\Downloads\\Resume Website\\templates"

replacements = {
    "templates\\\\resume\\\\delete_resume.html": [("{% url 'resume_list' %}", "{% url 'dashboard' %}")],
    "templates\\\\resume\\\\footer.html": [("{% url 'resume_list' %}", "{% url 'dashboard' %}")],
    "templates\\\\resume\\\\navbar.html": [("{% url 'resume_list' %}", "{% url 'dashboard' %}")],
    "templates\\\\website\\\\base.html": [("{% url 'resume_list' %}", "{% url 'template_list' %}")],
    "templates\\\\website\\\\blog_detail.html": [("{% url 'resume_list' %}", "{% url 'template_list' %}")],
    "templates\\\\website\\\\home.html": [("{% url 'resume_list' %}", "{% url 'template_list' %}")],
    "templates\\\\website\\\\navbar.html": [
        ("{% url 'resume_list' %}", "{% url 'dashboard' %}"),
        ("{% url 'blog' %}", "#")
    ],
    "templates\\\\website\\\\services.html": [("{% url 'resume_list' %}", "{% url 'template_list' %}")],
}

for rel_path, reps in replacements.items():
    full_path = os.path.join(dir_path, rel_path.replace("\\\\", "\\"))
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {rel_path}")

# Let's also globally find and fix any other 'blog' or 'resume_list'
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original = content
            content = content.replace("{% url 'resume_list' %}", "{% url 'template_list' %}")
            content = content.replace("{% url 'blog' %}", "#")
            if content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Globally Fixed {path}")
