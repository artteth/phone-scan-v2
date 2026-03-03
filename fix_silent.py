with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# 1. Fix default parameter - silent should be true
content = content.replace(
    'function syncFromGoogleSheets(silent = false) {',
    'function syncFromGoogleSheets(silent = true) {'
)

# 2. Remove the "Синхронизация..." toast - it should not show
old_sync = '''    isSyncing = true;
    console.log('🔄 Синхронизация...');
    
    // Show indicator
    const indicator = document.getElementById('sync-indicator');
    if (indicator) {
        indicator.classList.add('active');
    }'''

new_sync = '''    isSyncing = true;
    console.log('🔄 Синхронизация...');
    
    // Show indicator (no toast)
    const indicator = document.getElementById('sync-indicator');
    if (indicator) {
        indicator.classList.add('active');
    }'''

content = content.replace(old_sync, new_sync)

# 3. Make sure setInterval uses silent=true
old_interval = '''setInterval(() => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets();
            }
        }, 10000);'''

new_interval = '''setInterval(() => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets(true); // silent
            }
        }, 10000);'''

content = content.replace(old_interval, new_interval)

# 4. Make sure visibilitychange uses silent=true
old_visibility = '''document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets(true); // silent
            }
        });'''

# Already correct, but let's make sure
content = content.replace(
    "syncFromGoogleSheets(true); // silent",
    "syncFromGoogleSheets(true);"
)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Fixed silent sync')
