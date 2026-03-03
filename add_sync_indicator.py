with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# 1. Add CSS for sync indicator
css_style = '''        .toast.warning { background: var(--warning); }
        @keyframes toastSlideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .sync-indicator { position: fixed; top: 10px; right: 60px; background: var(--primary); color: white; padding: 8px 12px; border-radius: 20px; font-size: 0.85rem; display: none; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); z-index: 3000; animation: fadeIn 0.3s ease; }
        .sync-indicator.active { display: flex; }
        .sync-indicator .spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }'''

content = content.replace(
    '''        .toast.warning { background: var(--warning); }
        @keyframes toastSlideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }''',
    css_style
)

# 2. Add sync indicator HTML after header
html_indicator = '''            <header class="header">
                <button class="settings-btn" id="settings-btn">⚙️</button>
                <h1>📦 Сканер рулонов ткани</h1>
            </header>
            <div id="sync-indicator" class="sync-indicator">
                <span class="spinner"></span>
                <span>Синхронизация...</span>
            </div>'''

content = content.replace(
    '''            <header class="header">
                <button class="settings-btn" id="settings-btn">⚙️</button>
                <h1>📦 Сканер рулонов ткани</h1>
            </header>''',
    html_indicator
)

# 3. Update sync function to show/hide indicator
old_sync = '''function syncFromGoogleSheets(silent = true) {
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

content = content.replace(old_sync, new_sync)

# 4. Update callback to hide indicator
old_callback = '''window.handleGoogleSheetsResponse = function(response) {
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
        hideSyncIndicator();
    }
};'''

content = content.replace(old_callback, new_callback)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Sync indicator added')
