const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'; // Replace with your Google Sheet ID
const SHEET_NAME = 'рулоны';
const LOCK_TIMEOUT_SECONDS = 30;

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  const mode = e.parameter.mode || 'web';

  // JSONP mode for CORS bypass (GitHub Pages)
  if (mode === 'jsonp') {
    const callback = e.parameter.callback || 'callback';
    const action = e.parameter.action || 'getOrders';

    let result;
    try {
      if (action === 'getOrders') {
        result = getOrders();
      } else if (action === 'getOrder') {
        const orderId = e.parameter.orderId || '';
        result = getOrder(orderId);
      } else {
        result = { ok: false, error: 'Unknown action' };
      }
    } catch (err) {
      result = { ok: false, error: err.message };
    }

    const output = ContentService
      .createTextOutput(callback + '(' + JSON.stringify({ ok: true, data: result }) + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
    return output;
  }

  // JSON API for external frontend
  if (mode === 'tg-api') {
    const action = e.parameter.action || 'getOrders';
    if (action === 'getOrders') {
      return jsonResponse({ ok: true, data: getOrders() });
    } else if (action === 'getOrder') {
      const orderId = e.parameter.orderId || '';
      return jsonResponse({ ok: true, data: getOrder(orderId) });
    }
    return jsonResponse({ ok: false, error: 'Unknown action for GET' });
  }

  // Default: return web interface
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Fabric Inventory Scanner')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getSheet() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    // Headers: OrderID, RollNumber, FactoryLength, MeasuredLength, Shrinkage, Status, CreatedDate, ModifiedDate
    sheet.appendRow(['OrderID', 'RollNumber', 'FactoryLength', 'MeasuredLength', 'Shrinkage', 'Status', 'CreatedDate', 'ModifiedDate']);
  }
  return sheet;
}

function getOrders() {
  const sheet = getSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data.shift();

  const orders = {};

  data.forEach(row => {
    const orderId = String(row[0] || '');
    const rollNumber = parseInt(row[1]) || 0;
    
    if (!orderId) return;

    if (!orders[orderId]) {
      orders[orderId] = {
        id: orderId,
        totalRolls: 0,
        rolls: [],
        status: 'pending'
      };
    }

    const roll = {
      rollNumber: rollNumber,
      factoryLength: row[2] !== null && row[2] !== '' ? parseFloat(row[2]) : null,
      measuredLength: row[3] !== null && row[3] !== '' ? parseFloat(row[3]) : null,
      shrinkage: row[4] !== null && row[4] !== '' ? parseFloat(row[4]) : null,
      status: row[5] || 'pending',
      createdDate: row[6] ? formatDateForJS(row[6]) : '',
      modifiedDate: row[7] ? formatDateForJS(row[7]) : ''
    };

    orders[orderId].rolls.push(roll);
    orders[orderId].totalRolls = Math.max(orders[orderId].totalRolls, rollNumber);
  });

  // Sort rolls by rollNumber
  Object.values(orders).forEach(order => {
    order.rolls.sort((a, b) => a.rollNumber - b.rollNumber);
    updateOrderStatus(order);
  });

  return orders;
}

function getOrder(orderId) {
  const orders = getOrders();
  return orders[orderId] || null;
}

function updateOrderStatus(order) {
  const completedCount = order.rolls.filter(r => r.status === 'completed').length;
  const partialCount = order.rolls.filter(r => r.status === 'partial').length;

  if (completedCount === order.totalRolls && order.totalRolls > 0) {
    order.status = 'completed';
  } else if (completedCount > 0 || partialCount > 0) {
    order.status = 'in-progress';
  } else {
    order.status = 'pending';
  }
}

function formatDateForJS(dateVal) {
  if (!dateVal) return '';
  if (dateVal instanceof Date) {
    const year = dateVal.getFullYear();
    const month = String(dateVal.getMonth() + 1).padStart(2, '0');
    const day = String(dateVal.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }
  if (typeof dateVal === 'number') {
    const ms = Math.round((dateVal - 25569) * 86400 * 1000);
    const d = new Date(ms);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }
  return String(dateVal);
}

function generateId() {
  return 'roll_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function saveRoll(orderId, rollNumber, factoryLength, measuredLength, shrinkage) {
  const lock = LockService.getScriptLock();
  if (!lock) {
    throw new Error('Server busy. Please try again in a few seconds.');
  }
  try {
    const sheet = getSheet();
    const data = sheet.getDataRange().getValues();
    let rowIndex = -1;

    // Find existing row
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]) === String(orderId) && parseInt(data[i][1]) === parseInt(rollNumber)) {
        rowIndex = i + 1;
        break;
      }
    }

    // Determine status
    let status = 'pending';
    if (measuredLength !== null && shrinkage !== null) {
      status = 'completed';
    } else if (measuredLength !== null || shrinkage !== null) {
      status = 'partial';
    }

    const now = new Date();

    if (rowIndex > 0) {
      // Update existing row
      sheet.getRange(rowIndex, 3).setValue(factoryLength);
      sheet.getRange(rowIndex, 4).setValue(measuredLength);
      sheet.getRange(rowIndex, 5).setValue(shrinkage);
      sheet.getRange(rowIndex, 6).setValue(status);
      sheet.getRange(rowIndex, 8).setValue(now);
    } else {
      // Insert new row
      sheet.appendRow([
        orderId,
        rollNumber,
        factoryLength,
        measuredLength,
        shrinkage,
        status,
        now,
        now
      ]);
    }

    return getOrders();
  } finally {
    lock.releaseLock();
  }
}

function addOrder(orderId, totalRolls) {
  const lock = LockService.getScriptLock();
  if (!lock) {
    throw new Error('Server busy. Please try again in a few seconds.');
  }
  try {
    const sheet = getSheet();
    const now = new Date();

    // Create rolls for this order
    for (let i = 1; i <= totalRolls; i++) {
      sheet.appendRow([
        orderId,
        i,
        null,
        null,
        null,
        'pending',
        now,
        now
      ]);
    }

    return getOrders();
  } finally {
    lock.releaseLock();
  }
}

function deleteRoll(orderId, rollNumber) {
  const lock = LockService.getScriptLock();
  if (!lock) {
    throw new Error('Server busy. Please try again in a few seconds.');
  }
  try {
    const sheet = getSheet();
    const data = sheet.getDataRange().getValues();

    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]) === String(orderId) && parseInt(data[i][1]) === parseInt(rollNumber)) {
        sheet.deleteRow(i + 1);
        break;
      }
    }

    return getOrders();
  } finally {
    lock.releaseLock();
  }
}

// POST handler for API requests
function doPost(e) {
  try {
    const isTgApi = (e.parameter && e.parameter.mode === 'tg-api');

    if (!isTgApi && e.postData && e.postData.contents) {
      try {
        const payloadCheck = JSON.parse(e.postData.contents);
        if (payloadCheck._tgApiMode === true) {
          isTgApi = true;
        }
      } catch (ee) {}
    }

    if (isTgApi) {
      const payloadRaw = e.postData && e.postData.contents ? e.postData.contents : '{}';
      const payload = JSON.parse(payloadRaw);
      const action = payload.action;

      if (action === 'getOrders') {
        return jsonResponse({ ok: true, data: getOrders() });
      } else if (action === 'getOrder') {
        const orderId = payload.orderId || '';
        return jsonResponse({ ok: true, data: getOrder(orderId) });
      } else if (action === 'saveRoll') {
        const orderId = payload.orderId || '';
        const rollNumber = payload.rollNumber || 0;
        const factoryLength = payload.factoryLength || null;
        const measuredLength = payload.measuredLength || null;
        const shrinkage = payload.shrinkage || null;
        const data = saveRoll(orderId, rollNumber, factoryLength, measuredLength, shrinkage);
        return jsonResponse({ ok: true, data });
      } else if (action === 'addOrder') {
        const orderId = payload.orderId || '';
        const totalRolls = payload.totalRolls || 0;
        const data = addOrder(orderId, totalRolls);
        return jsonResponse({ ok: true, data });
      } else if (action === 'deleteRoll') {
        const orderId = payload.orderId || '';
        const rollNumber = payload.rollNumber || 0;
        const data = deleteRoll(orderId, rollNumber);
        return jsonResponse({ ok: true, data });
      }

      return jsonResponse({ ok: false, error: 'Unknown action' });
    }

    // Fallback for non-API requests
    if (!e.postData || !e.postData.contents) {
      return ContentService.createTextOutput('OK');
    }

    const contents = e.postData.contents;
    const update = JSON.parse(contents);

    if (update.action === 'saveRoll') {
      const orderId = update.orderId || '';
      const rollNumber = update.rollNumber || 0;
      const factoryLength = update.factoryLength || null;
      const measuredLength = update.measuredLength || null;
      const shrinkage = update.shrinkage || null;
      const data = saveRoll(orderId, rollNumber, factoryLength, measuredLength, shrinkage);
      return jsonResponse({ ok: true, data });
    }

    return ContentService.createTextOutput('OK');
  } catch (error) {
    return ContentService.createTextOutput('Error: ' + error.message);
  }
}
