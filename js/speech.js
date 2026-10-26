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

    // One shared context: browsers cap open contexts (~6 in Chrome) and start them suspended
    let sharedCtx = null;
    function getAudioContext() {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return null;
        if (!sharedCtx || sharedCtx.state === 'closed') sharedCtx = new AudioCtx();
        if (sharedCtx.state === 'suspended') sharedCtx.resume().catch(() => {});
        return sharedCtx;
    }

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
            const ctx = getAudioContext();
            if (!ctx) return;
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
        } catch (e) {
            console.warn('Sound effect failed:', e);
        }
    }

    // ---- Text-to-speech ----
    const ttsSupported = 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';
    let voices = [];
    let speakTimer = null;
    let currentUtterance = null; // keep a reference, Chrome may garbage-collect it mid-speech
    let warnedNoVoice = false;

    function loadVoices() {
        if (!ttsSupported) return;
        voices = window.speechSynthesis.getVoices() || [];
    }
    if (ttsSupported) {
        loadVoices();
        if (typeof window.speechSynthesis.addEventListener === 'function') {
            window.speechSynthesis.addEventListener('voiceschanged', loadVoices);
        } else {
            window.speechSynthesis.onvoiceschanged = loadVoices;
        }
    }

    function pickVoice() {
        return voices.find(v => v.lang === 'en-US')
            || voices.find(v => v.lang === 'en-GB')
            || voices.find(v => /^en[-_]/i.test(v.lang) || v.lang === 'en')
            || null;
    }

    function notify(msg) {
        if (typeof showToast === 'function') showToast(msg);
        else console.warn(msg);
    }

    function isSpeechSupported() {
        return ttsSupported;
    }

    /**
     * Pronounce English text using Web Speech API
     */
    function speak(text, rate = 0.9) {
        if (!ttsSupported) {
            notify('Speech is not supported in this browser.');
            return false;
        }
        const clean = String(text || '').replace(/_+/g, 'blank').trim();
        if (!clean) return false;

        const synth = window.speechSynthesis;
        clearTimeout(speakTimer);

        const run = () => {
            try {
                if (synth.paused) synth.resume();
                loadVoices();
                const utter = new SpeechSynthesisUtterance(clean);
                const voice = pickVoice();
                if (voice) {
                    utter.voice = voice;
                    utter.lang = voice.lang;
                } else {
                    utter.lang = 'en-US';
                    if (voices.length === 0 && !warnedNoVoice) {
                        warnedNoVoice = true;
                        notify('No speech voices found. Install a system TTS voice (e.g. speech-dispatcher / espeak-ng on Linux).');
                    }
                }
                utter.rate = rate;
                utter.onerror = (ev) => {
                    if (ev.error && ev.error !== 'canceled' && ev.error !== 'interrupted') {
                        notify('Speech failed: ' + ev.error);
                    }
                };
                currentUtterance = utter;
                synth.speak(utter);
            } catch (e) {
                console.warn('Speech failed:', e);
            }
        };

        // cancel() immediately followed by speak() is dropped by Chrome, so give it a tick
        if (synth.speaking || synth.pending) {
            synth.cancel();
            speakTimer = setTimeout(run, 80);
        } else {
            run();
        }
        return true;
    }

    return {
        isSoundEnabled,
        toggleSound,
        playSound,
        speak,
        isSpeechSupported
    };
})();
