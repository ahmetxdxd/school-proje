// js/storage.js
// Multi-Language Memory & Vocabulary CRUD Manager

const StorageManager = (() => {
    const SUPPORTED_LANGUAGES = {
        tr: { name: 'Türkçe', flag: '🇹🇷', label: 'Turkish' },
        es: { name: 'Español', flag: '🇪🇸', label: 'Spanish' },
        de: { name: 'Deutsch', flag: '🇩🇪', label: 'German' },
        fr: { name: 'Français', flag: '🇫🇷', label: 'French' },
        it: { name: 'Italiano', flag: '🇮🇹', label: 'Italian' },
        ar: { name: 'العربية', flag: '🇸🇦', label: 'Arabic' }
    };

    function getActiveLanguage() {
        const lang = localStorage.getItem('lexiflow_active_lang') || 'tr';
        return SUPPORTED_LANGUAGES[lang] ? lang : 'tr';
    }

    function setActiveLanguage(lang) {
        if (SUPPORTED_LANGUAGES[lang]) {
            localStorage.setItem('lexiflow_active_lang', lang);
        }
    }

    function getVocabularyKey(lang = getActiveLanguage()) {
        return `lexiflow_vocab_${lang}`;
    }

    function getStatsKey(lang = getActiveLanguage()) {
        return `lexiflow_stats_${lang}`;
    }

    function getMistakesKey(lang = getActiveLanguage()) {
        return `lexiflow_mistakes_${lang}`;
    }

    // ---- Per-language translation cache (non-Turkish profiles only) ----
    // The built-in dataset carries Turkish meanings only. Other languages keep the
    // English fields and get their own `tr` meaning filled in from this cache.
    function wordKey(word) {
        return String(word || '').toLowerCase().trim();
    }

    function getTransCache(lang = getActiveLanguage()) {
        try {
            const raw = localStorage.getItem(`lexiflow_transcache_${lang}`);
            if (raw) return JSON.parse(raw) || {};
        } catch (e) {}
        return {};
    }

    function saveTransCache(cache, lang = getActiveLanguage()) {
        try {
            localStorage.setItem(`lexiflow_transcache_${lang}`, JSON.stringify(cache));
        } catch (e) {}
    }

    function seedVocabulary(lang) {
        const initial = JSON.parse(JSON.stringify(DEFAULT_VOCABULARY));
        if (lang !== 'tr') {
            const cache = getTransCache(lang);
            initial.forEach(w => {
                w.tr = cache[wordKey(w.word)] || '';
                w.trLang = lang;
            });
        }
        return initial;
    }

    // Older builds copied the Turkish list into every language profile: blank those meanings
    function migrateForeignMeanings(words, lang) {
        if (lang === 'tr') return false;
        const cache = getTransCache(lang);
        let changed = false;
        words.forEach(w => {
            if (!w.custom && w.trLang !== lang) {
                w.tr = cache[wordKey(w.word)] || '';
                w.trLang = lang;
                changed = true;
            }
        });
        return changed;
    }

    function getVocabulary(lang = getActiveLanguage()) {
        try {
            const raw = localStorage.getItem(getVocabularyKey(lang));
            if (raw) {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    if (migrateForeignMeanings(parsed, lang)) saveVocabulary(parsed, lang);
                    return parsed;
                }
            }
        } catch (e) {
            console.error('Error loading vocabulary from localStorage:', e);
        }

        // Initialize with default vocabulary
        if (typeof DEFAULT_VOCABULARY !== 'undefined' && Array.isArray(DEFAULT_VOCABULARY)) {
            const initial = seedVocabulary(lang);
            saveVocabulary(initial, lang);
            return initial;
        }
        return [];
    }

    // Fill empty meanings from { lowercasedWord: translation } without clobbering concurrent edits
    function applyTranslations(map, lang = getActiveLanguage()) {
        const vocab = getVocabulary(lang);
        let changed = 0;
        vocab.forEach(w => {
            const t = map[wordKey(w.word)];
            if (t && !w.tr) {
                w.tr = t;
                w.trLang = lang;
                changed++;
            }
        });
        if (changed) saveVocabulary(vocab, lang);
        return changed;
    }

    function saveVocabulary(words, lang = getActiveLanguage()) {
        try {
            localStorage.setItem(getVocabularyKey(lang), JSON.stringify(words));
        } catch (e) {
            console.error('Error saving vocabulary to localStorage:', e);
        }
    }

    function addWord(wordObj, lang = getActiveLanguage()) {
        const vocab = getVocabulary(lang);
        const newId = vocab.length > 0 ? Math.max(...vocab.map(w => w.id || 0)) + 1 : 1;
        const newWord = {
            id: newId,
            unit: wordObj.unit || 'Custom',
            unitTitle: wordObj.unitTitle || (wordObj.unit ? `${wordObj.unit}: Custom Added` : 'Custom: User Added'),
            section: wordObj.section || 'General',
            word: wordObj.word.trim(),
            pos: wordObj.pos ? wordObj.pos.trim() : '(n)',
            definition: wordObj.definition ? wordObj.definition.trim() : '',
            example: wordObj.example ? wordObj.example.trim() : '',
            tr: wordObj.tr ? wordObj.tr.trim() : '',
            derivatives: Array.isArray(wordObj.derivatives) ? wordObj.derivatives : [],
            imageUrl: wordObj.imageUrl || '',
            custom: true,
            createdAt: new Date().toISOString()
        };
        vocab.unshift(newWord);
        saveVocabulary(vocab, lang);
        return newWord;
    }

    function deleteWord(wordId, lang = getActiveLanguage()) {
        const vocab = getVocabulary(lang);
        const filtered = vocab.filter(w => w.id !== wordId);
        saveVocabulary(filtered, lang);
        return filtered;
    }

    function updateWord(updatedObj, lang = getActiveLanguage()) {
        const vocab = getVocabulary(lang);
        const index = vocab.findIndex(w => w.id === updatedObj.id);
        if (index !== -1) {
            vocab[index] = { ...vocab[index], ...updatedObj };
            saveVocabulary(vocab, lang);
            return vocab[index];
        }
        return null;
    }

    function resetVocabulary(lang = getActiveLanguage()) {
        if (typeof DEFAULT_VOCABULARY !== 'undefined') {
            const initial = seedVocabulary(lang);
            saveVocabulary(initial, lang);
            return initial;
        }
        return [];
    }

    function getStats(lang = getActiveLanguage()) {
        try {
            const raw = localStorage.getItem(getStatsKey(lang));
            if (raw) return JSON.parse(raw);
        } catch (e) {}
        return {
            streak: 0,
            bestStreak: 0,
            totalSolved: 0,
            correct: 0,
            wrong: 0,
            lastSessionDate: null
        };
    }

    function saveStats(stats, lang = getActiveLanguage()) {
        try {
            localStorage.setItem(getStatsKey(lang), JSON.stringify(stats));
        } catch (e) {}
    }

    function getMistakes(lang = getActiveLanguage()) {
        try {
            const raw = localStorage.getItem(getMistakesKey(lang));
            if (raw) return JSON.parse(raw);
        } catch (e) {}
        return [];
    }

    function saveMistakes(mistakes, lang = getActiveLanguage()) {
        try {
            localStorage.setItem(getMistakesKey(lang), JSON.stringify(mistakes));
        } catch (e) {}
    }

    function exportJSON(lang = getActiveLanguage()) {
        const vocab = getVocabulary(lang);
        const stats = getStats(lang);
        const bundle = {
            appName: 'LexiFlow',
            version: '2.0.0',
            exportedAt: new Date().toISOString(),
            language: lang,
            stats: stats,
            vocabulary: vocab
        };
        return JSON.stringify(bundle, null, 2);
    }

    function importJSON(jsonString, lang = getActiveLanguage()) {
        try {
            const parsed = JSON.parse(jsonString);
            if (Array.isArray(parsed)) {
                saveVocabulary(parsed, lang);
                return { success: true, count: parsed.length };
            } else if (parsed && Array.isArray(parsed.vocabulary)) {
                saveVocabulary(parsed.vocabulary, lang);
                if (parsed.stats) saveStats(parsed.stats, lang);
                return { success: true, count: parsed.vocabulary.length };
            }
            return { success: false, error: 'Invalid JSON schema' };
        } catch (e) {
            return { success: false, error: e.message };
        }
    }

    return {
        SUPPORTED_LANGUAGES,
        getActiveLanguage,
        setActiveLanguage,
        getVocabulary,
        saveVocabulary,
        getTransCache,
        saveTransCache,
        applyTranslations,
        addWord,
        deleteWord,
        updateWord,
        resetVocabulary,
        getStats,
        saveStats,
        getMistakes,
        saveMistakes,
        exportJSON,
        importJSON
    };
})();
