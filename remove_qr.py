import re

FILE = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

with open(FILE, 'r') as f:
    content = f.read()

# 1. Remove QR codes button
content = re.sub(r'\s*<button id="view-qr-codes-btn" class="btn btn-outline">🔲 QR-коды</button>', '', content)

# 2. Remove QR codes page
content = re.sub(r'\s*<div id="qr-codes-page" class="page">.*?</div>\n    </div>\n    <script>', '\n    </div>\n    <script>', content, flags=re.DOTALL)

# 3. Remove renderQRCodePage call
content = content.replace('renderQRCodePage();', '')

# 4. Remove renderQRCodePage function
content = re.sub(r'function renderQRCodePage\(\)\{[^}]*\}\}', '', content, flags=re.DOTALL)

# 5. Remove TEST_CODES
content = re.sub(r'const TEST_CODES = \[[^\]]*\];', '', content, flags=re.DOTALL)

# 6. Remove view-qr-codes-btn listener
content = content.replace("document.getElementById('view-qr-codes-btn').addEventListener('click',()=>showPage('qr-codes-page'));", '')

# 7. Remove QRCode CDN
content = content.replace('    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>\n', '')

# 8. Remove any remaining QR references
content = re.sub(r'qr-code-item|qr-codes-grid|qr-code-label|qr-\w+', '', content, flags=re.IGNORECASE)

with open(FILE, 'w') as f:
    f.write(content)

print('QR codes completely removed')
