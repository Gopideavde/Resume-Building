import os
import shutil

dir_path = "C:\\Users\\GOPI\\Downloads\\Resume Website\\templates"

# 1. Replace strings in all html files
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            original = content
            content = content.replace("website/base.html", "core/base.html")
            content = content.replace("website/navbar.html", "core/navbar.html")
            content = content.replace("website/footer.html", "core/footer.html")
            if content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated references in {path}")

# 2. Move files from website/ to core/
website_dir = os.path.join(dir_path, "website")
core_dir = os.path.join(dir_path, "core")

if os.path.exists(website_dir):
    for file in os.listdir(website_dir):
        src = os.path.join(website_dir, file)
        dst = os.path.join(core_dir, file)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            os.remove(src)
            print(f"Moved {file} to core/")
    os.rmdir(website_dir)
    print("Deleted website/ directory")
