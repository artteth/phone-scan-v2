with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Add timeout to saveToGoogleSheets
old_save_func = '''function saveToGoogleSheets(action, payload) {
    return new Promise((resolve, reject) => {
        const data = {
            _tgApiMode: true,
            action: action,
            ...payload
        };
        
        fetch(GOOGLE_APPS_SCRIPT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: JSON.stringify(data),
            redirect: 'follow'
        })
        .then(response => response.json())
        .then(result => {
            if (result.ok) {
                orders = result.data;
                saveData();
                resolve(result);
            } else {
                reject(new Error(result.error || 'Save failed'));
            }
        })
        .catch(err => {
            console.error('Google Sheets save error:', err);
            reject(err);
        });
    });
}'''

new_save_func = '''function saveToGoogleSheets(action, payload) {
    return new Promise((resolve, reject) => {
        const data = {
            _tgApiMode: true,
            action: action,
            ...payload
        };
        
        console.log('📡 Sending to Google Sheets:', action);
        
        // Timeout after 5 seconds
        const timeoutId = setTimeout(() => {
            console.log('⏰ Google Sheets timeout - falling back to local save');
            reject(new Error('Timeout'));
        }, 5000);
        
        fetch(GOOGLE_APPS_SCRIPT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: JSON.stringify(data),
            redirect: 'follow'
        })
        .then(response => {
            console.log('📥 Response status:', response.status);
            return response.json();
        })
        .then(result => {
            clearTimeout(timeoutId);
            console.log('📊 Result:', result);
            if (result.ok) {
                orders = result.data;
                saveData();
                resolve(result);
            } else {
                reject(new Error(result.error || 'Save failed'));
            }
        })
        .catch(err => {
            clearTimeout(timeoutId);
            console.error('❌ Google Sheets save error:', err);
            reject(err);
        });
    });
}'''

content = content.replace(old_save_func, new_save_func)

# Update saveRollData to handle timeout better
old_save_data = '''.catch(err => {
            console.error('❌ Failed to save to Google Sheets:', err);
            submitBtn.classList.remove('saving');
            submitBtn.classList.add('error');
            submitBtn.textContent = '✗ Ошибка';
            playScanError();
            setTimeout(() => {
                submitBtn.classList.remove('btn-loading', 'error', 'saving');
                submitBtn.textContent = originalText;
                saveData();
                closeRecordModal();
                showToast('Данные сохранены локально (ошибка синхронизации)', 'warning');
                if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
            }, 500);
        });'''

new_save_data = '''.catch(err => {
            console.error('❌ Failed to save to Google Sheets:', err);
            // Always save locally if Google Sheets fails
            saveData();
            submitBtn.classList.remove('saving');
            submitBtn.classList.add('success');
            submitBtn.textContent = '✓ Сохранено (локально)';
            playScanSuccess();
            setTimeout(() => {
                submitBtn.classList.remove('btn-loading', 'success', 'saving');
                submitBtn.textContent = originalText;
                closeRecordModal();
                showToast('Данные сохранены локально', 'success');
                if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
            }, 500);
        });'''

content = content.replace(old_save_data, new_save_data)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added timeout and better error handling')
