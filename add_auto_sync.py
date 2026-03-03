with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Add auto-sync interval after initial sync
old_init = '''    // Sync from Google Sheets if enabled
    if (USE_GOOGLE_SHEETS) {
        syncFromGoogleSheets();
    } else {
        renderOrdersList();
    }'''

new_init = '''    // Sync from Google Sheets if enabled
    if (USE_GOOGLE_SHEETS) {
        syncFromGoogleSheets();
        // Auto-sync every 30 seconds
        setInterval(() => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets();
            }
        }, 30000);
        // Sync when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                syncFromGoogleSheets();
            }
        });
    } else {
        renderOrdersList();
    }'''

content = content.replace(old_init, new_init)

# Also update sync function to not show toast on auto-sync
old_sync_func = '''function syncFromGoogleSheets() {
    if (!GOOGLE_APPS_SCRIPT_URL) {
        console.error('No Google Apps Script URL configured');
        showToast('Ошибка: нет URL скрипта', 'error');
        return;
    }
    if (isSyncing) {
        console.log('Already syncing...');
        return;
    }
    
    isSyncing = true;
    showToast('Синхронизация...', 'info');'''

new_sync_func = '''function syncFromGoogleSheets(silent = false) {
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
    }'''

content = content.replace(old_sync_func, new_sync_func)

# Update callback to use silent mode
old_callback = '''window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    console.log('📥 Ответ от Google Sheets:', response);
    
    if (response && response.ok && response.data) {
        orders = response.data;
        console.log('✅ Загружено заказов:', Object.keys(orders).length);
        console.log('Заказы:', orders);
        saveData();
        renderOrdersList();
        showToast('Данные обновлены', 'success');
    } else {
        console.error('❌ Ошибка: response=', response);
        showToast('Ошибка загрузки данных', 'error');
    }
};'''

new_callback = '''window.handleGoogleSheetsResponse = function(response) {
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

content = content.replace(old_callback, new_callback)

# Update manual sync button to use non-silent mode
old_btn = '''document.getElementById('sync-now-btn').addEventListener('click', () => {
        syncFromGoogleSheets();
    });'''

new_btn = '''document.getElementById('sync-now-btn').addEventListener('click', () => {
        syncFromGoogleSheets(false); // false = show toast
    });'''

content = content.replace(old_btn, new_btn)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Auto-sync added')
