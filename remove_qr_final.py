import re

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Remove renderQRCodePage call
content = content.replace('renderQRCodePage();', '')

# Remove renderQRCodePage function  
content = re.sub(r'function renderQRCodePage\(\)\{[^}]*\}\}', '', content, flags=re.DOTALL)

# Remove TEST_CODES
content = re.sub(r'const TEST_CODES = \[[^\]]*\];', '', content, flags=re.DOTALL)

# Remove view-qr-codes-btn listener
content = content.replace("document.getElementById('view-qr-codes-btn').addEventListener('click',()=>showPage('qr-codes-page'));", '')

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('QR code code removed')
