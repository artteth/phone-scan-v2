with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Find openScanner function and add audio context initialization
old_open_scanner = '''function openScanner(){const modal=document.getElementById('scanner-modal');modal.classList.add('active');if(!html5QrcodeScanner){html5QrcodeScanner=new Html5QrcodeScanner('qr-reader',{fps:10,qrbox:{width:250,height:250}},false);} html5QrcodeScanner.render(handleQRCodeScan,(error)=>{console.log('Scanner error:',error);});}'''

new_open_scanner = '''function openScanner(){
    // Initialize audio context on first user interaction (required for iOS)
    if (!window.scanAudioContext) {
        try {
            window.scanAudioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('✅ Audio context initialized');
        } catch (e) {
            console.log('❌ Audio context error:', e);
        }
    }
    const modal=document.getElementById('scanner-modal');modal.classList.add('active');if(!html5QrcodeScanner){html5QrcodeScanner=new Html5QrcodeScanner('qr-reader',{fps:10,qrbox:{width:250,height:250}},false);} html5QrcodeScanner.render(handleQRCodeScan,(error)=>{console.log('Scanner error:',error);});
}'''

content = content.replace(old_open_scanner, new_open_scanner)

# Also update playScanSuccess to resume audio context
old_success = '''function playScanSuccess() {
    console.log('🔊 Playing scan success feedback');
    // Vibration
    if (navigator.vibrate) {
        navigator.vibrate(100);
        console.log('📳 Vibration triggered');
    } else {
        console.log('❌ Vibration not supported');
    }
    // Beep sound - create audio context on first user interaction
    try {
        if (!window.scanAudioContext) {
            window.scanAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        const audioContext = window.scanAudioContext;'''

new_success = '''function playScanSuccess() {
    console.log('🔊 Playing scan success feedback');
    // Vibration
    if (navigator.vibrate) {
        navigator.vibrate(100);
        console.log('📳 Vibration triggered');
    } else {
        console.log('❌ Vibration not supported');
    }
    // Beep sound
    try {
        if (!window.scanAudioContext) {
            window.scanAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        const audioContext = window.scanAudioContext;
        // Resume audio context if suspended (required for iOS)
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }'''

content = content.replace(old_success, new_success)

# Update playScanError too
old_error = '''function playScanError() {
    console.log('🔊 Playing scan error feedback');
    // Vibration - two buzzes
    if (navigator.vibrate) {
        navigator.vibrate([200, 100, 200]);
        console.log('📳 Error vibration triggered');
    }
    // Error sound
    try {
        if (!window.scanAudioContext) {
            window.scanAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        const audioContext = window.scanAudioContext;'''

new_error = '''function playScanError() {
    console.log('🔊 Playing scan error feedback');
    // Vibration - two buzzes
    if (navigator.vibrate) {
        navigator.vibrate([200, 100, 200]);
        console.log('📳 Error vibration triggered');
    }
    // Error sound
    try {
        if (!window.scanAudioContext) {
            window.scanAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        const audioContext = window.scanAudioContext;
        // Resume audio context if suspended (required for iOS)
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }'''

content = content.replace(old_error, new_error)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Fixed audio context initialization for iOS')
