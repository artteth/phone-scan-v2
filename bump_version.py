#!/usr/bin/env python3
"""
Автоматическое увеличение версии при каждом обновлении

Использование:
    python3 bump_version.py [major|minor|patch]
    
По умолчанию: minor (v2.2 → v2.3)
"""

import re
import sys
import subprocess
from datetime import datetime

def get_current_version():
    """Get current version from README"""
    with open('README.md', 'r') as f:
        content = f.read()
    match = re.search(r'\*\*Версия:\*\* (\d+)\.(\d+)', content)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 2, 2

def bump_version(bump_type='minor'):
    """Increase version"""
    major, minor = get_current_version()
    
    if bump_type == 'major':
        major += 1
        minor = 0
    elif bump_type == 'minor':
        minor += 1
    elif bump_type == 'patch':
        minor += 1  # We use minor for patches
    
    new_version = f"v{major}.{minor}"
    return major, minor, new_version

def update_files(major, minor, new_version):
    """Update version in all files"""
    
    # Update README
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Update version at top
    content = re.sub(
        r'\*\*Версия:\*\* \d+\.\d+',
        f'**Версия:** {major}.{minor}',
        content
    )
    
    # Update version table
    old_table_line = f"| v{major}.{minor-1} |"
    new_table_line = f"| v{major}.{minor} | Добавлен номер версии в заголовок |\n| v{major}.{minor-1} |"
    content = content.replace(old_table_line, new_table_line)
    
    # Update history
    date = datetime.now().strftime("%B %Y")
    history_entry = f"""### Версия {new_version} ({date})
- ✅ Автоматическое обновление версии

"""
    content = content.replace('### Версия 2.2 (Март 2024)', history_entry + '### Версия 2.2 (Март 2024)')
    
    with open('README.md', 'w') as f:
        f.write(content)
    
    # Update index.html
    with open('index.html', 'r') as f:
        content = f.read()
    
    content = re.sub(
        r'v\d+</span>',
        f'{new_version}</span>',
        content
    )
    
    with open('index.html', 'w') as f:
        f.write(content)
    
    print(f'Version bumped to {new_version}')
    return new_version

def main():
    bump_type = sys.argv[1] if len(sys.argv) > 1 else 'minor'
    major, minor, new_version = bump_version(bump_type)
    update_files(major, minor, new_version)
    
    # Git commit
    subprocess.run(['git', 'add', '-A'])
    subprocess.run(['git', 'commit', '-m', f'Bump version to {new_version}'])
    subprocess.run(['git', 'push'])
    
    print(f'✅ GitHub updated to {new_version}')

if __name__ == '__main__':
    main()
