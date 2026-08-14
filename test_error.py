import urllib.request
import time
import subprocess

# Start server
proc = subprocess.Popen(["C:\\Users\\GOPI\\Downloads\\Resume Website\\env\\Scripts\\python.exe", "manage.py", "runserver"])
time.sleep(4)

url = "http://127.0.0.1:8000/"

try:
    response = urllib.request.urlopen(url)
    print(f"{url} -> {response.status}")
except Exception as e:
    print(f"{url} -> Error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode())

proc.kill()
