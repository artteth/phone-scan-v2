with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'r') as f:
    content = f.read()

# Replace playScanSuccess with simpler version
old_success = '''function playScanSuccess() {
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
}'''

new_success = '''function playScanSuccess() {
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
        const audioContext = window.scanAudioContext;
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 1000;
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.5, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
        console.log('🔊 Beep played');
    } catch (e) {
        console.log('❌ Audio error:', e);
    }
}'''

content = content.replace(old_success, new_success)

# Replace playScanError
old_error = '''function playScanError() {
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
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 150;
        oscillator.type = 'square';
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
        console.log('🔊 Error beep played');
    } catch (e) {
        console.log('❌ Audio error:', e);
    }
}'''

content = content.replace(old_error, new_error)

with open('/Users/artem/Documents/phone scan v2/основной проект/index.html', 'w') as f:
    f.write(content)

print('Added debug logging to scan feedback')
