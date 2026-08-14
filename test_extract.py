import urllib.request
import time
import subprocess
import re

proc = subprocess.Popen(["C:\\Users\\GOPI\\Downloads\\Resume Website\\env\\Scripts\\python.exe", "manage.py", "runserver", "--noreload"])
time.sleep(3)

url = "http://127.0.0.1:8000/about/"

try:
    urllib.request.urlopen(url)
except Exception as e:
    if hasattr(e, 'read'):
        html = e.read().decode('utf-8', errors='ignore')
        match2 = re.search(r"Exception Value:(.*?)</pre>", html, re.DOTALL | re.IGNORECASE)
        if match2:
            print("EXCEPTION:", match2.group(1).strip())
        
        match3 = re.search(r"In template .*?, error at line <strong>(.*?)</strong>(.*?)<br>", html, re.DOTALL)
        if match3:
            print("TEMPLATE LINE:", match3.group(1))
            print("TEMPLATE MSG:", match3.group(2).strip())

proc.kill()
