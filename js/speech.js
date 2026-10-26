// js/speech.js
// Speech Synthesis (TTS) & Web Audio Sound Effects

const AudioManager = (() => {
    let soundEnabled = true;

    // Load persisted sound preference
    try {
        const saved = localStorage.getItem('lexiflow_sound_enabled');
        if (saved !== null) {
            soundEnabled = saved === 'true';
        }
    } catch (e) {}

    function isSoundEnabled() {
        return soundEnabled;
    }

    function toggleSound() {
        soundEnabled = !soundEnabled;
        try {
            localStorage.setItem('lexiflow_sound_enabled', String(soundEnabled));
        } catch (e) {}
        return soundEnabled;
    }

    /**
     * Synthesize game audio chords via Web Audio API (100% offline, zero network latency)
     */
    function playSound(type) {
        if (!soundEnabled) return;
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const now = ctx.currentTime;

            if (type === 'correct') {
                // Cheerful 4-note ascending chord (C5 -> E5 -> G5 -> C6)
                [523.25, 659.25, 783.99, 1046.50].forEach((freq, idx) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, now + (idx * 0.07));
                    gain.gain.setValueAtTime(0.12, now + (idx * 0.07));
                    gain.gain.exponentialRampToValueAtTime(0.001, now + (idx * 0.07) + 0.35);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + (idx * 0.07));
                    osc.stop(now + (idx * 0.07) + 0.35);
                });
            } else if (type === 'wrong') {
                // Gentle 2-note descending buzz
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(280, now);
                osc.frequency.setValueAtTime(210, now + 0.12);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.38);
            } else if (type === 'click') {
                // Subtle tactile click
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, now);
                gain.gain.setValueAtTime(0.04, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.05);
            } else if (type === 'fanfare') {
                // Celebration victory fanfare
                const chord = [523.25, 659.25, 783.99, 1046.50, 1318.51];
                chord.forEach((freq, idx) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, now + (idx * 0.1));
                    gain.gain.setValueAtTime(0.14, now + (idx * 0.1));
                    gain.gain.exponentialRampToValueAtTime(0.001, now + (idx * 0.1) + 0.5);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + (idx * 0.1));
                    osc.stop(now + (idx * 0.1) + 0.5);
                });
            }
        } catch (e) {}
    }

    /**
     * Pronounce English text using Web Speech API
     */
    function speak(text, rate = 0.9) {
        if (!('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            const clean = text.replace(/_+/g, 'blank').trim();
            const utter = new SpeechSynthesisUtterance(clean);
            utter.lang = 'en-US';
            utter.rate = rate;
            window.speechSynthesis.speak(utter);
        } catch (e) {}
    }

    return {
        isSoundEnabled,
        toggleSound,
        playSound,
        speak
    };
})();
