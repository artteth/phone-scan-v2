with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Update sync function - silent by default, only show errors
old_sync = '''function syncFromGoogleSheets(silent = false) {
    if (!GOOGLE_APPS_SCRIPT_URL) {
        if (!silent) {
            console.error('No Google Apps Script URL configured');
            showToast('Ошибка: нет URL скрипта', 'error');
        }
        return;
    }
    if (isSyncing) {
        return;
    }
    
    isSyncing = true;
    if (!silent) {
        showToast('Синхронизация...', 'info');
        console.log('🔄 Запрос данных из Google Sheets...');
    }
    
    console.log('URL:', GOOGLE_APPS_SCRIPT_URL);
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('❌ Ошибка загрузки скрипта');
        showToast('Ошибка синхронизации', 'error');
    };
    document.head.appendChild(script);
}'''

new_sync = '''function syncFromGoogleSheets(silent = true) {
    if (!GOOGLE_APPS_SCRIPT_URL) {
        if (!silent) {
            console.error('No Google Apps Script URL configured');
            showToast('Ошибка: нет URL скрипта', 'error');
        }
        return;
    }
    if (isSyncing) {
        return;
    }
    
    isSyncing = true;
    console.log('🔄 Авто-синхронизация...');
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('❌ Ошибка загрузки скрипта');
        if (!silent) {
            showToast('Ошибка синхронизации', 'error');
        }
    };
    document.head.appendChild(script);
}'''

content = content.replace(old_sync, new_sync)

# Update callback - no success toast on auto-sync
old_callback = '''window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    
    if (response && response.ok && response.data) {
        orders = response.data;
        console.log('✅ Синхронизация:', Object.keys(orders).length, 'заказов');
        saveData();
        renderOrdersList();
    } else {
        console.error('❌ Ошибка синхронизации:', response);
    }
};'''

new_callback = '''window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    
    if (response && response.ok && response.data) {
        orders = response.data;
        console.log('✅ Обновлено:', Object.keys(orders).length, 'заказов');
        saveData();
        renderOrdersList();
    } else {
        console.error('❌ Ошибка синхронизации:', response);
    }
};'''

content = content.replace(old_callback, new_callback)

# Update manual sync button - show notifications
old_btn = '''document.getElementById('sync-now-btn').addEventListener('click', () => {
        syncFromGoogleSheets(false); // false = show toast
    });'''

new_btn = '''document.getElementById('sync-now-btn').addEventListener('click', () => {
        syncFromGoogleSheets(false); // false = show notifications
    });'''

content = content.replace(old_btn, new_btn)

# Update visibility change - silent
old_visibility = '''document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets();
            }
        });'''

new_visibility = '''document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets(true); // silent
            }
        });'''

content = content.replace(old_visibility, new_visibility)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Silent sync enabled')
