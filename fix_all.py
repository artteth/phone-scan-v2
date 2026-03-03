import re

FILE = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

with open(FILE, 'r') as f:
    content = f.read()

# === 1. Fix gsEnabled ===
content = content.replace("let USE_GOOGLE_SHEETS = gsEnabled === 'true';", "let USE_GOOGLE_SHEETS = true;")

# === 2. Fix loadSettings ===
content = content.replace(
    "GOOGLE_APPS_SCRIPT_URL = gsUrl || GOOGLE_APPS_SCRIPT_URL;",
    "if (gsUrl && gsUrl !== '') { GOOGLE_APPS_SCRIPT_URL = gsUrl; }"
)

# === 3. Fix CORS ===
content = content.replace("fetch(GOOGLE_APPS_SCRIPT_URL + '?mode=tg-api', {", "fetch(GOOGLE_APPS_SCRIPT_URL, {")
content = content.replace("'Content-Type': 'application/json'", "'Content-Type': 'text/plain'")
content = content.replace("body: JSON.stringify(data)\n        })", "body: JSON.stringify(data),\n            redirect: 'follow'\n        })")

# === 4. Remove QR button ===
content = content.replace('<button id="view-qr-codes-btn" class="btn btn-outline">🔲 QR-коды</button>\n', '')

# === 5. Remove QR listener ===
content = content.replace("document.getElementById('view-qr-codes-btn').addEventListener('click',()=>showPage('qr-codes-page'));", '')

# === 6. Remove renderQRCodePage call ===
content = content.replace('renderQRCodePage();', '')

# === 7. Remove QRCode CDN ===
content = content.replace('    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>\n', '')

# === VALIDATE ===
errors = []
if content.count('{') != content.count('}'):
    errors.append(f"Brace mismatch: {content.count('{')} open, {content.count('}')} close")

if errors:
    print('VALIDATION FAILED:')
    for e in errors:
        print(f'  - {e}')
    print(f'\nDebug: {content.count("{")} open, {content.count("}")} close')
    exit(1)

with open(FILE, 'w') as f:
    f.write(content)

print('✅ All fixes applied!')
print(f'   Braces: {content.count("{")} open, {content.count("}")} close')
