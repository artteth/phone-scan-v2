#!/usr/bin/env python3
"""Safe fix for index.html"""
import re

FILE = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

with open(FILE, 'r') as f:
    content = f.read()

# Fix 1: gsEnabled
content = content.replace("let USE_GOOGLE_SHEETS = gsEnabled === 'true';", "let USE_GOOGLE_SHEETS = true;")

# Fix 2: loadSettings
content = content.replace("GOOGLE_APPS_SCRIPT_URL = gsUrl || GOOGLE_APPS_SCRIPT_URL;", "if(gsUrl&&gsUrl!==''){GOOGLE_APPS_SCRIPT_URL=gsUrl;}")

# Fix 3: CORS
content = content.replace("fetch(GOOGLE_APPS_SCRIPT_URL + '?mode=tg-api', {", "fetch(GOOGLE_APPS_SCRIPT_URL, {")
content = content.replace("'Content-Type': 'application/json'", "'Content-Type': 'text/plain'")
content = content.replace("body: JSON.stringify(data)\n        })", "body: JSON.stringify(data),\n            redirect: 'follow'\n        })")

# Validate
if content.count('{') != content.count('}'):
    print(f"ERROR: Brace mismatch: {content.count('{')} open, {content.count('}')} close")
    exit(1)

with open(FILE, 'w') as f:
    f.write(content)

print("Fixes applied successfully!")
