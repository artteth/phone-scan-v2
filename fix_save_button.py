with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Fix saveRollData to handle undefined USE_GOOGLE_SHEETS
old_save = '''function saveRollData(complete){
    const factoryLength=parseFloat(document.getElementById('factory-length').value);
    const measuredLength=parseFloat(document.getElementById('measured-length').value)||null;
    const shrinkage=parseFloat(document.getElementById('shrinkage').value)||null;
    if(isNaN(factoryLength)){showToast('Введите заводской метраж','error');return;}
    const order=orders[currentOrderId];
    let roll=order.rolls.find(r=>r.rollNumber===currentRollNumber);
    if(!roll){roll={rollNumber:currentRollNumber,factoryLength,measuredLength:null,shrinkage:null,status:'pending'};order.rolls.push(roll);}
    roll.factoryLength=factoryLength;
    if(measuredLength!==null&&shrinkage!==null){roll.measuredLength=measuredLength;roll.shrinkage=shrinkage;roll.status='completed';}
    else if(measuredLength!==null||shrinkage!==null){roll.measuredLength=measuredLength;roll.shrinkage=shrinkage;roll.status='partial';}
    else{roll.status='pending';}
    updateOrderStatus(order);
    
    // Save to Google Sheets if enabled
    if (USE_GOOGLE_SHEETS && GOOGLE_APPS_SCRIPT_URL) {
        saveToGoogleSheets('saveRoll', {
            orderId: currentOrderId,
            rollNumber: currentRollNumber,
            factoryLength: factoryLength,
            measuredLength: measuredLength,
            shrinkage: shrinkage
        })
        .then(() => {
            closeRecordModal();
            showToast('Данные сохранены в Google Таблицу', 'success');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        })
        .catch(err => {
            console.error('Failed to save to Google Sheets:', err);
            saveData();
            closeRecordModal();
            showToast('Данные сохранены локально (ошибка синхронизации)', 'warning');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        });
    } else {
        saveData();
        closeRecordModal();
        showToast('Данные сохранены', 'success');
        if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
    }
}'''

new_save = '''function saveRollData(complete){
    console.log('💾 saveRollData called');
    const factoryLength=parseFloat(document.getElementById('factory-length').value);
    const measuredLength=parseFloat(document.getElementById('measured-length').value)||null;
    const shrinkage=parseFloat(document.getElementById('shrinkage').value)||null;
    if(isNaN(factoryLength)){
        playScanError();
        showToast('Введите заводской метраж','error');
        console.log('❌ Invalid factory length');
        return;
    }
    console.log('✅ Factory length:', factoryLength);
    const order=orders[currentOrderId];
    let roll=order.rolls.find(r=>r.rollNumber===currentRollNumber);
    if(!roll){roll={rollNumber:currentRollNumber,factoryLength,measuredLength:null,shrinkage:null,status:'pending'};order.rolls.push(roll);}
    roll.factoryLength=factoryLength;
    if(measuredLength!==null&&shrinkage!==null){roll.measuredLength=measuredLength;roll.shrinkage=shrinkage;roll.status='completed';}
    else if(measuredLength!==null||shrinkage!==null){roll.measuredLength=measuredLength;roll.shrinkage=shrinkage;roll.status='partial';}
    else{roll.status='pending';}
    updateOrderStatus(order);
    
    console.log('📊 USE_GOOGLE_SHEETS:', typeof USE_GOOGLE_SHEETS, USE_GOOGLE_SHEETS);
    console.log('🔗 GOOGLE_APPS_SCRIPT_URL:', typeof GOOGLE_APPS_SCRIPT_URL, GOOGLE_APPS_SCRIPT_URL ? 'defined' : 'undefined');
    
    // Save to Google Sheets if enabled
    if (typeof USE_GOOGLE_SHEETS !== 'undefined' && USE_GOOGLE_SHEETS && typeof GOOGLE_APPS_SCRIPT_URL !== 'undefined' && GOOGLE_APPS_SCRIPT_URL) {
        console.log('☁️ Saving to Google Sheets...');
        saveToGoogleSheets('saveRoll', {
            orderId: currentOrderId,
            rollNumber: currentRollNumber,
            factoryLength: factoryLength,
            measuredLength: measuredLength,
            shrinkage: shrinkage
        })
        .then(() => {
            console.log('✅ Saved to Google Sheets');
            playScanSuccess();
            closeRecordModal();
            showToast('Данные сохранены в Google Таблицу', 'success');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        })
        .catch(err => {
            console.error('❌ Failed to save to Google Sheets:', err);
            playScanError();
            saveData();
            closeRecordModal();
            showToast('Данные сохранены локально (ошибка синхронизации)', 'warning');
            if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
        });
    } else {
        console.log('💾 Saving locally...');
        playScanSuccess();
        saveData();
        closeRecordModal();
        showToast('Данные сохранены', 'success');
        if(document.getElementById('order-detail-page').classList.contains('active')){renderOrderDetail(currentOrderId);}
    }
}'''

content = content.replace(old_save, new_save)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added debug logging to saveRollData')
