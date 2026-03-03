import re

FILE = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

with open(FILE, 'r') as f:
    content = f.read()

# 1. Remove renderQRCodePage call
content = content.replace('renderQRCodePage();', '')

# 2. Remove renderQRCodePage function
content = re.sub(r'function renderQRCodePage\(\)\{[^}]*\}\}', '', content, flags=re.DOTALL)

# 3. Remove view-qr-codes-btn listener
content = content.replace("document.getElementById('view-qr-codes-btn').addEventListener('click',()=>showPage('qr-codes-page'));", '')

# 4. Fix isSyncing timeout
old_sync = '''function syncFromGoogleSheets() {
    if (isSyncing || !GOOGLE_APPS_SCRIPT_URL) {
        console.log('Sync skipped:', {isSyncing, hasUrl: !!GOOGLE_APPS_SCRIPT_URL});
        return;
    }
    
    isSyncing = true;
    showToast('Синхронизация...', 'info');
    console.log('Syncing from:', GOOGLE_APPS_SCRIPT_URL);
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('Sync error: script failed to load');
        showToast('Ошибка синхронизации', 'error');
    };
    document.head.appendChild(script);
}'''

new_sync = '''function syncFromGoogleSheets() {
    if (!GOOGLE_APPS_SCRIPT_URL) {
        console.log('Sync skipped: no URL');
        return;
    }
    
    if (isSyncing) {
        console.log('Sync skipped: already syncing');
        return;
    }
    
    isSyncing = true;
    showToast('Синхронизация...', 'info');
    console.log('Syncing from:', GOOGLE_APPS_SCRIPT_URL);
    
    // Timeout to reset isSyncing after 10 seconds
    setTimeout(() => { isSyncing = false; }, 10000);
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('Sync error: script failed to load');
        showToast('Ошибка синхронизации', 'error');
    };
    document.head.appendChild(script);
}'''

content = content.replace(old_sync, new_sync)

with open(FILE, 'w') as f:
    f.write(content)

print('Fixed')
