with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Fix: Make sure hideSyncIndicator is defined before it's called
# Find the sync function and add hideSyncIndicator right after it

old_sync_block = '''function syncFromGoogleSheets(silent = true) {
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
    console.log('🔄 Синхронизация...');
    
    // Show indicator
    const indicator = document.getElementById('sync-indicator');
    if (indicator) {
        indicator.classList.add('active');
    }
    
    const script = document.createElement('script');
    script.src = GOOGLE_APPS_SCRIPT_URL + '?action=getOrders&mode=jsonp&callback=handleGoogleSheetsResponse';
    script.onerror = function() {
        isSyncing = false;
        console.error('❌ Ошибка загрузки скрипта');
        if (indicator) indicator.classList.remove('active');
        if (!silent) {
            showToast('Ошибка синхронизации', 'error');
        }
    };
    document.head.appendChild(script);
}

function hideSyncIndicator() {
    const indicator = document.getElementById('sync-indicator');
    if (indicator) {
        indicator.classList.remove('active');
    }
}'''

# Check if this exists, if not we need to add it properly
if 'function hideSyncIndicator()' not in content:
    # Add hideSyncIndicator after syncFromGoogleSheets
    content = content.replace(
        "document.head.appendChild(script);\n}",
        "document.head.appendChild(script);\n}\n\nfunction hideSyncIndicator() {\n    const indicator = document.getElementById('sync-indicator');\n    if (indicator) {\n        indicator.classList.remove('active');\n    }\n}"
    )
    print('Added hideSyncIndicator function')
else:
    print('hideSyncIndicator already exists')

# Fix callback to use hideSyncIndicator
old_callback = '''window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    hideSyncIndicator();
    
    if (response && response.ok && response.data) {
        orders = response.data;
        console.log('✅ Обновлено:', Object.keys(orders).length, 'заказов');
        saveData();
        renderOrdersList();
    } else {
        console.error('❌ Ошибка синхронизации:', response);
        hideSyncIndicator();
    }
};'''

new_callback = '''window.handleGoogleSheetsResponse = function(response) {
    isSyncing = false;
    hideSyncIndicator();
    
    if (response && response.ok && response.data) {
        orders = response.data;
        console.log('✅ Обновлено:', Object.keys(orders).length, 'заказов');
        saveData();
        renderOrdersList();
    } else {
        console.error('❌ Ошибка синхронизации:', response);
    }
    hideSyncIndicator();
};'''

content = content.replace(old_callback, new_callback)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Fixed hideSyncIndicator')
