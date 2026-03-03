with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# 1. Add CSS for loading button with progress bar
css_loading = '''        .form-actions .btn { flex: 1; }
        .btn-loading { position: relative; overflow: hidden; pointer-events: none; opacity: 0.8; }
        .btn-loading::after { content: ''; position: absolute; bottom: 0; left: 0; height: 3px; background: rgba(255,255,255,0.7); width: 0%; transition: width 0.3s ease; }
        .btn-loading.saving::after { width: 100%; transition: width 2s ease-in-out; }
        .btn-loading.success { background: var(--success) !important; }
        .btn-loading.error { background: var(--danger) !important; }'''

content = content.replace(
    '.form-actions .btn { flex: 1; }',
    '.form-actions .btn { flex: 1; }' + css_loading
)

# 2. Add button press feedback function
old_feedback = '''// Scan feedback - vibration and sound
function playScanSuccess() {'''

new_feedback = '''// Button press feedback
function playButtonPress() {
    if (navigator.vibrate) {
        navigator.vibrate(30);
    }
}

// Scan feedback - vibration and sound
function playScanSuccess() {'''

content = content.replace(old_feedback, new_feedback)

# 3. Update saveRollData to show loading state
old_save_start = '''function saveRollData(complete){
    console.log('💾 saveRollData called');
    const factoryLength=parseFloat(document.getElementById('factory-length').value);'''

new_save_start = '''function saveRollData(complete){
    console.log('💾 saveRollData called');
    
    // Get submit button and show loading state
    const submitBtn = document.querySelector('#record-form button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.classList.add('btn-loading', 'saving');
    submitBtn.textContent = 'Сохранение...';
    playButtonPress();
    
    const factoryLength=parseFloat(document.getElementById('factory-length').value);'''

content = content.replace(old_save_start, new_save_start)

# 4. Update success callback
old_success = '''.then(() => {
            console.log('✅ Saved to Google Sheets');
            playScanSuccess();
            closeRecordModal();
            showToast('Данные сохранены в Google Таблицу', 'success');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        })'''

new_success = '''.then(() => {
            console.log('✅ Saved to Google Sheets');
            submitBtn.classList.remove('saving');
            submitBtn.classList.add('success');
            submitBtn.textContent = '✓ Сохранено';
            playScanSuccess();
            setTimeout(() => {
                submitBtn.classList.remove('btn-loading', 'success', 'saving');
                submitBtn.textContent = originalText;
                closeRecordModal();
                showToast('Данные сохранены в Google Таблицу', 'success');
                if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
            }, 500);
        })'''

content = content.replace(old_success, new_success)

# 5. Update error callback
old_error = '''.catch(err => {
            console.error('❌ Failed to save to Google Sheets:', err);
            playScanError();
            saveData();
            closeRecordModal();
            showToast('Данные сохранены локально (ошибка синхронизации)', 'warning');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        });'''

new_error = '''.catch(err => {
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

content = content.replace(old_error, new_error)

# 6. Update local save path
old_local = '''    } else {
        console.log('💾 Saving locally...');
        playScanSuccess();
        saveData();
        closeRecordModal();
        showToast('Данные сохранены', 'success');
        if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
    }'''

new_local = '''    } else {
        console.log('💾 Saving locally...');
        submitBtn.classList.remove('saving');
        submitBtn.classList.add('success');
        submitBtn.textContent = '✓ Сохранено';
        playScanSuccess();
        setTimeout(() => {
            submitBtn.classList.remove('btn-loading', 'success', 'saving');
            submitBtn.textContent = originalText;
            saveData();
            closeRecordModal();
            showToast('Данные сохранены', 'success');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        }, 500);
    }'''

content = content.replace(old_local, new_local)

# 7. Add vibration to save-partial button
old_partial = "document.getElementById('save-partial').addEventListener('click',handlePartialSave);"
new_partial = "document.getElementById('save-partial').addEventListener('click',function(){playButtonPress();handlePartialSave();});"
content = content.replace(old_partial, new_partial)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added button press feedback with vibration and loading animation')
