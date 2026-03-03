with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Add scan feedback functions after showToast function
old_toast_end = '''function showToast(message,type='info'){let container=document.querySelector('.toast-container');if(!container){container=document.createElement('div');container.className='toast-container';document.body.appendChild(container);}const toast=document.createElement('div');toast.className='toast '+type;toast.textContent=message;container.appendChild(toast);setTimeout(()=>{toast.remove();},3000);}'''

new_toast_end = '''function showToast(message,type='info'){let container=document.querySelector('.toast-container');if(!container){container=document.createElement('div');container.className='toast-container';document.body.appendChild(container);}const toast=document.createElement('div');toast.className='toast '+type;toast.textContent=message;container.appendChild(toast);setTimeout(()=>{toast.remove();},3000);}

// Scan feedback - vibration and sound
function playScanSuccess() {
    // Vibration pattern: short buzz
    if (navigator.vibrate) {
        navigator.vibrate(50);
    }
    // Beep sound
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 880; // A5 note
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.15);
    } catch (e) {
        console.log('Audio not supported');
    }
}

function playScanError() {
    // Vibration pattern: two short buzzes
    if (navigator.vibrate) {
        navigator.vibrate([100, 50, 100]);
    }
    // Error sound (lower tone)
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 220; // A3 note (lower)
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    } catch (e) {
        console.log('Audio not supported');
    }
}'''

content = content.replace(old_toast_end, new_toast_end)

# Update handleQRCodeScan to play success sound
content = content.replace(
    'function handleQRCodeScan(decodedText){closeScanner();processScannedCode(decodedText);}',
    'function handleQRCodeScan(decodedText){closeScanner();playScanSuccess();processScannedCode(decodedText);}'
)

# Update processScannedCode to play error sound on errors
content = content.replace(
    "showToast('Неверный формат кода. Используйте формат: НОМЕР_РУЛОН (например, 2020_1)','error');",
    "playScanError();showToast('Неверный формат кода. Используйте формат: НОМЕР_РУЛОН (например, 2020_1)','error');"
)

content = content.replace(
    "showToast('Неверный номер рулона','error');",
    "playScanError();showToast('Неверный номер рулона','error');"
)

content = content.replace(
    "showToast('Неверное количество рулонов','error');",
    "playScanError();showToast('Неверное количество рулонов','error');"
)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added scan feedback (vibration + sound)')
