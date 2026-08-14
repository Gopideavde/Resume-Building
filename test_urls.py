import urllib.request
import time
import subprocess

# Start server
proc = subprocess.Popen(["C:\\Users\\GOPI\\Downloads\\Resume Website\\env\\Scripts\\python.exe", "manage.py", "runserver"])
time.sleep(4)

urls_to_test = [
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/templates/",
    "http://127.0.0.1:8000/about/",
    "http://127.0.0.1:8000/contact/"
]

for url in urls_to_test:
    try:
        response = urllib.request.urlopen(url)
        print(f"{url} -> {response.status}")
    except Exception as e:
        print(f"{url} -> Error: {e}")

proc.kill()
