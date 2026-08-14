import os
import re

dir_path = "C:\\Users\\GOPI\\Downloads\\Resume Website\\templates"

replacements = {
    "{% url 'services' %}": "#",
    "{% url 'faq' %}": "#",
    "{% url 'terms_conditions' %}": "{% url 'terms' %}",
    "{% url 'subscribe_newsletter' %}": "#"
}

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original = content
            for old, new in replacements.items():
                content = content.replace(old, new)
            if content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Globally Fixed {path}")
