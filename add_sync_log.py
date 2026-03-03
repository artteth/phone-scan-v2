import re

FILE = '/Users/artem/Documents/phone scan v2/основной проект/index.html'

with open(FILE, 'r') as f:
    content = f.read()

# Add logging to sync function
old_sync = '''function syncFromGoogleSheets() {
    if (isSyncing || !GOOGLE_APPS_SCRIPT_URL) return;
    
    isSyncing = true;
    showToast('Синхронизация...', 'info');
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        showToast('Ошибка синхронизации', 'error');
    };
    document.head.appendChild(script);
}'''

new_sync = '''function syncFromGoogleSheets() {
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
}

window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    console.log('Sync response:', response);
    
    if (response && response.ok && response.data) {
        orders = response.data;
        saveData();
        renderOrdersList();
        showToast('Данные обновлены', 'success');
        console.log('Orders loaded:', Object.keys(orders).length);
    } else {
        console.error('Sync error:', response);
        showToast('Ошибка загрузки данных', 'error');
    }
};'''

content = content.replace(old_sync, new_sync)

# Remove duplicate handleGoogleSheetsResponse
content = re.sub(r'// Global callback for JSONP\s*window\.handleGoogleSheetsResponse = function\(response\) \{[^}]+\};', '', content)

with open(FILE, 'w') as f:
    f.write(content)

print('Logging added')
