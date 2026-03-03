with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Add logging to sync
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
}

// Global callback for JSONP
window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    
    if (response && response.ok && response.data) {
        orders = response.data;
        saveData();
        renderOrdersList();
        showToast('Данные обновлены', 'success');
    } else {
        console.error('Google Sheets response error:', response);
        showToast('Ошибка загрузки данных', 'error');
    }
};'''

new_sync = '''function syncFromGoogleSheets() {
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
    showToast('Синхронизация...', 'info');
    console.log('🔄 Запрос данных из Google Sheets...');
    console.log('URL:', GOOGLE_APPS_SCRIPT_URL);
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('❌ Ошибка загрузки скрипта');
        showToast('Ошибка синхронизации', 'error');
    };
    document.head.appendChild(script);
}

// Global callback for JSONP
window.handleGoogleSheetsResponse = function(response) {
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

content = content.replace(old_sync, new_sync)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Logging added')
