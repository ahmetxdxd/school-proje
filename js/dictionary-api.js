// js/dictionary-api.js
// Auto Dictionary Lookup & Image Fetcher Service

const DictionaryService = (() => {
    // Cache for API responses to avoid duplicate network requests
    const cache = {
        dict: {},
        trans: {},
        images: {}
    };

    /**
     * Fetch English Definition, Part of Speech, Audio and Example from FreeDictionary API
     */
    async function lookupEnglishWord(rawWord) {
        const word = rawWord.trim().toLowerCase();
        if (!word) return null;

        if (cache.dict[word]) {
            return cache.dict[word];
        }

        try {
            const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`;
            const response = await fetch(url);
            if (!response.ok) {
                return null;
            }
            const data = await response.json();
            if (!Array.isArray(data) || data.length === 0) return null;

            const entry = data[0];
            let pos = '(n)';
            let definition = '';
            let example = '';
            let audioUrl = '';
            const derivatives = [];

            // Extract audio if available
            if (Array.isArray(entry.phonetics)) {
                for (const ph of entry.phonetics) {
                    if (ph.audio && ph.audio.trim().length > 0) {
                        audioUrl = ph.audio;
                        break;
                    }
                }
            }

            // Extract meanings
            if (Array.isArray(entry.meanings) && entry.meanings.length > 0) {
                const firstMeaning = entry.meanings[0];
                const rawPos = firstMeaning.partOfSpeech || 'noun';
                if (rawPos.startsWith('v')) pos = '(v)';
                else if (rawPos.startsWith('adj')) pos = '(adj)';
                else if (rawPos.startsWith('adv')) pos = '(adv)';
                else pos = '(n)';

                if (Array.isArray(firstMeaning.definitions) && firstMeaning.definitions.length > 0) {
                    definition = firstMeaning.definitions[0].definition || '';
                    example = firstMeaning.definitions[0].example || '';
                }

                // If first meaning didn't have example, look in other definitions
                if (!example) {
                    for (const m of entry.meanings) {
                        if (Array.isArray(m.definitions)) {
                            for (const d of m.definitions) {
                                if (d.example) {
                                    example = d.example;
                                    break;
                                }
                            }
                        }
                        if (example) break;
                    }
                }

                // Collect other parts of speech as derivatives
                entry.meanings.forEach(m => {
                    if (m.partOfSpeech && m.partOfSpeech !== rawPos) {
                        derivatives.push(`${m.partOfSpeech}: ${entry.word}`);
                    }
                });
            }

            // If no example from dictionary, craft a clean contextual fallback
            if (!example && definition) {
                example = `Academic researchers often examine how ${word} impacts contemporary systems.`;
            }

            const result = {
                word: entry.word || word,
                pos,
                definition,
                example,
                audioUrl,
                derivatives: [...new Set(derivatives)]
            };

            cache.dict[word] = result;
            return result;
        } catch (e) {
            console.warn('Dictionary API request failed:', e);
            return null;
        }
    }

    /**
     * Translate English word to target language (Turkish, Spanish, German, French, etc.)
     */
    async function translateWord(rawWord, targetLang = 'tr') {
        const word = rawWord.trim();
        if (!word) return '';

        const cacheKey = `${word}_${targetLang}`;
        if (cache.trans[cacheKey]) return cache.trans[cacheKey];

        try {
            const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(word)}&langpair=en|${encodeURIComponent(targetLang)}`;
            const response = await fetch(url);
            if (!response.ok) return '';
            const data = await response.json();
            if (data && data.responseData && data.responseData.translatedText) {
                let trans = data.responseData.translatedText.trim().toLowerCase();
                // If translation returned identical word, check matches
                if (trans.toLowerCase() === word.toLowerCase() && Array.isArray(data.matches)) {
                    for (const m of data.matches) {
                        if (m.translation && m.translation.toLowerCase() !== word.toLowerCase()) {
                            trans = m.translation.trim().toLowerCase();
                            break;
                        }
                    }
                }
                cache.trans[cacheKey] = trans;
                return trans;
            }
        } catch (e) {
            console.warn('Translation API request failed:', e);
        }
        return '';
    }

    /**
     * Fetch a Wikipedia thumbnail for a word. Resolves to null when there is none
     * (or when offline) so callers can fall back to a different question type.
     */
    async function fetchWordImage(rawWord) {
        const word = rawWord.trim().toLowerCase();
        if (!word) return null;

        if (word in cache.images) return cache.images[word];

        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 4000);
        try {
            const wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(word)}`;
            const res = await fetch(wikiUrl, { signal: ctrl.signal });
            if (res.ok) {
                const data = await res.json();
                if (data.type !== 'disambiguation' && data.thumbnail && data.thumbnail.source) {
                    cache.images[word] = data.thumbnail.source;
                    return data.thumbnail.source;
                }
            }
            cache.images[word] = null; // definitively no image
        } catch (e) {
            // network error / timeout: do not cache, may work later
        } finally {
            clearTimeout(timer);
        }
        return null;
    }

    return {
        lookupEnglishWord,
        translateWord,
        fetchWordImage
    };
})();
