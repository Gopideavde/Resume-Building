import urllib.request
import time
import subprocess
import os

proc = subprocess.Popen(
    ["C:\\Users\\GOPI\\Downloads\\Resume Website\\env\\Scripts\\python.exe", "manage.py", "runserver", "--noreload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(3)

url = "http://127.0.0.1:8000/"

try:
    urllib.request.urlopen(url)
except Exception as e:
    pass

time.sleep(1)
proc.terminate()
outs, errs = proc.communicate(timeout=5)
print("--- STDOUT ---")
print(outs)
