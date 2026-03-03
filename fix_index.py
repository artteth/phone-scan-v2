#!/usr/bin/env python3
"""
Fix index.html - Safe version
This script applies fixes without breaking JavaScript
"""
import re

FILE_PATH = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

def main():
    with open(FILE_PATH, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # === FIX 1: Fix gsEnabled reference ===
    content = content.replace(
        "let USE_GOOGLE_SHEETS = gsEnabled === 'true';",
        "let USE_GOOGLE_SHEETS = true; // Fixed: was gsEnabled reference"
    )
    
    # === FIX 2: Fix loadSettings to use default URL ===
    content = content.replace(
        "GOOGLE_APPS_SCRIPT_URL = gsUrl || GOOGLE_APPS_SCRIPT_URL;",
        "if (gsUrl && gsUrl !== '') { GOOGLE_APPS_SCRIPT_URL = gsUrl; }"
    )
    
    # === FIX 3: Fix CORS - remove mode=tg-api ===
    content = content.replace(
        "fetch(GOOGLE_APPS_SCRIPT_URL + '?mode=tg-api', {",
        "fetch(GOOGLE_APPS_SCRIPT_URL, {"
    )
    
    # === FIX 4: Fix CORS - change Content-Type to text/plain ===
    content = content.replace(
        "'Content-Type': 'application/json'",
        "'Content-Type': 'text/plain'"
    )
    
    # === FIX 5: Add redirect: follow ===
    content = content.replace(
        "body: JSON.stringify(data)\n        })",
        "body: JSON.stringify(data),\n            redirect: 'follow'\n        })"
    )
    
    # === VALIDATION ===
    errors = []
    
    # Check braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    if open_braces != close_braces:
        errors.append(f'Brace mismatch: {open_braces} open, {close_braces} close')
    
    # Check for gsEnabled without definition
    if 'gsEnabled ===' in content and 'const gsEnabled' not in content and 'let gsEnabled' not in content:
        errors.append('gsEnabled used without definition')
    
    if errors:
        print('ERRORS FOUND - NOT SAVING:')
        for err in errors:
            print(f'  - {err}')
        return False
    
    # Save
    with open(FILE_PATH, 'w') as f:
        f.write(content)
    
    changes = content != original_content
    print(f'Fixes applied: {changes}')
    print('Validation: PASSED')
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
