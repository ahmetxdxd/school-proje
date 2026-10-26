// js/translations.js
// Background translation of the built-in word list for non-Turkish language profiles.
// Turkish meanings ship with the dataset; every other language is translated on demand,
// cached in localStorage and resumable (the free API has a daily quota).

const TranslationService = (() => {
    const CONCURRENCY = 3;
    const REQUEST_TIMEOUT_MS = 8000;
    const running = {};
    const lastStatus = {}; // lang -> 'done' | 'quota' | 'offline' | 'idle'
    let listener = null;

    function onChange(fn) {
        listener = fn;
    }

    function emit(lang) {
        if (typeof listener === 'function') listener(lang, getProgress(lang));
    }

    function getProgress(lang = StorageManager.getActiveLanguage()) {
        const vocab = StorageManager.getVocabulary(lang);
        const done = vocab.filter(w => w.tr).length;
        return {
            lang,
            total: vocab.length,
            done,
            running: !!running[lang],
            status: lastStatus[lang] || 'idle'
        };
    }

    async function fetchOne(word, lang) {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), REQUEST_TIMEOUT_MS);
        try {
            const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(word)}&langpair=en|${encodeURIComponent(lang)}`;
            const res = await fetch(url, { signal: ctrl.signal });
            if (res.status === 429) return { quota: true };
            if (!res.ok) return { error: true };
            const data = await res.json();
            const text = data && data.responseData && data.responseData.translatedText;
            if (Number(data.responseStatus) === 429 || /MYMEMORY WARNING|QUERY LENGTH LIMIT/i.test(text || '')) {
                return { quota: true };
            }
            if (!text) return { error: true };

            let best = text.trim();
            // Prefer the best-quality match when the primary answer just echoes the English word
            if (best.toLowerCase() === word.toLowerCase() && Array.isArray(data.matches)) {
                const alt = data.matches.find(m => m.translation && m.translation.trim().toLowerCase() !== word.toLowerCase());
                if (alt) best = alt.translation.trim();
            }
            return { text: best };
        } catch (e) {
            return { offline: true };
        } finally {
            clearTimeout(timer);
        }
    }

    /**
     * Translate every word of `lang` that has no meaning yet. Safe to call repeatedly.
     */
    async function run(lang = StorageManager.getActiveLanguage()) {
        if (lang === 'tr' || running[lang]) return getProgress(lang);

        const cache = StorageManager.getTransCache(lang);
        // Words already in the cache but missing from the profile (e.g. after a reset)
        StorageManager.applyTranslations(cache, lang);

        const queue = StorageManager.getVocabulary(lang)
            .filter(w => !w.tr)
            .map(w => w.word);

        if (queue.length === 0) {
            lastStatus[lang] = 'done';
            emit(lang);
            return getProgress(lang);
        }

        running[lang] = true;
        lastStatus[lang] = 'idle';
        emit(lang);

        let stop = null; // 'quota' | 'offline'
        let pendingBatch = {};
        let sinceFlush = 0;

        const flush = () => {
            if (sinceFlush === 0) return;
            StorageManager.saveTransCache(cache, lang);
            StorageManager.applyTranslations(pendingBatch, lang);
            pendingBatch = {};
            sinceFlush = 0;
            emit(lang);
        };

        const worker = async () => {
            while (!stop && queue.length > 0) {
                const word = queue.shift();
                const out = await fetchOne(word, lang);
                if (out.quota) { stop = 'quota'; break; }
                if (out.offline) { stop = 'offline'; break; }
                if (out.text) {
                    const key = word.toLowerCase().trim();
                    cache[key] = out.text;
                    pendingBatch[key] = out.text;
                    if (++sinceFlush >= 10) flush();
                }
            }
        };

        await Promise.all(Array.from({ length: CONCURRENCY }, worker));
        flush();

        running[lang] = false;
        lastStatus[lang] = stop || (getProgress(lang).done >= getProgress(lang).total ? 'done' : 'idle');
        emit(lang);
        return getProgress(lang);
    }

    return { run, getProgress, onChange };
})();
