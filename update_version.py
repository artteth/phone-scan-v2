with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Update title in header - add version
content = content.replace(
    '<h1>📦 Сканер рулонов ткани</h1>',
    '<h1>📦 Сканер рулонов ткани <span style="font-size: 0.7em; opacity: 0.8; font-weight: normal;">v2</span></h1>'
)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added v2 to header')
