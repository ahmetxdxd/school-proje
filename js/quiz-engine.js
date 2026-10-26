// js/quiz-engine.js
// Advanced Gamified Quiz Engine (Derivatives, Definitions, Sentences, Audio & Images)

const QuizEngine = (() => {
    let state = {
        active: false,
        vocabularyPool: [],
        questionQueue: [],
        currentIndex: 0,
        totalCount: 0,
        score: 0,
        wrong: 0,
        streak: 0,
        bestStreak: 0,
        answered: false,
        selectedOption: null,
        activeQuestion: null,
        history: [],
        mistakes: []
    };

    // Supported Question Types
    const QUESTION_TYPES = {
        mixed: { label: '🔀 Mixed Mode (All Varieties)', desc: 'Sentences, Derivatives, Definitions, Audio & Images' },
        sentence: { label: '📝 Sentence Fill-in', desc: 'Find the missing word in context sentences' },
        derivatives: { label: '🔤 Word Forms & Derivatives', desc: 'Second forms, Noun / Verb / Adjective derivations' },
        def_to_word: { label: '📖 Definition ➔ Word', desc: 'Identify the academic word matching the definition' },
        word_to_def: { label: '🇬🇧 Word ➔ Definition', desc: 'Select the accurate English definition' },
        meaning: { label: '🌐 Word ➔ Meaning', desc: 'Match word with your active language meaning' },
        listening: { label: '🎧 Listening Practice', desc: 'Listen to the audio and identify the word' },
        image_match: { label: '🖼️ Visual Matching', desc: 'Match images and concepts to academic words' }
    };

    function shuffle(arr) {
        const copy = [...arr];
        for (let i = copy.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copy[i], copy[j]] = [copy[j], copy[i]];
        }
        return copy;
    }

    // Helper: Blank out target word in sentence cleanly without regex escape bugs
    function blankSentence(sentence, word) {
        if (!sentence || !word) return { display: sentence || '', raw: sentence || '' };
        const tokens = sentence.split(/(\s+|[.,!?;:'"()]+)/);
        const targetLower = word.toLowerCase().trim();
        let replaced = false;
        const result = tokens.map(token => {
            const clean = token.toLowerCase().replace(/[^a-z]/g, '');
            if (!replaced && clean.length >= 3 && targetLower.length >= 3) {
                if (clean === targetLower || (clean.startsWith(targetLower) && clean.length <= targetLower.length + 4) || (targetLower.startsWith(clean) && targetLower.length <= clean.length + 3)) {
                    replaced = true;
                    return '<span class="sentence-blank">__________</span>';
                }
            }
            return token;
        }).join('');

        if (replaced) return { display: result, raw: sentence };
        return { display: sentence + ' <span class="sentence-blank">__________</span>', raw: sentence };
    }

    // Helper: Highlight target word in sentence
    function highlightSentence(sentence, word) {
        if (!sentence || !word) return sentence || '';
        const tokens = sentence.split(/(\s+|[.,!?;:'"()]+)/);
        const targetLower = word.toLowerCase().trim();
        let replaced = false;
        return tokens.map(token => {
            const clean = token.toLowerCase().replace(/[^a-z]/g, '');
            if (!replaced && clean.length >= 3 && targetLower.length >= 3) {
                if (clean === targetLower || (clean.startsWith(targetLower) && clean.length <= targetLower.length + 4) || (targetLower.startsWith(clean) && targetLower.length <= clean.length + 3)) {
                    replaced = true;
                    return '<span class="highlight-word">' + token + '</span>';
                }
            }
            return token;
        }).join('');
    }

    // Generate smart morphological distractor options for derivatives
    function generateDerivativeDistractors(baseWord, targetDeriv) {
        const cleanBase = baseWord.toLowerCase().replace(/[^a-z]/g, '');
        const suffixes = ['tion', 'ment', 'able', 'ive', 'ance', 'ence', 'ity', 'ly', 'ize', 'ing', 'ed'];
        const candidates = new Set();

        suffixes.forEach(s => {
            let fake = cleanBase + s;
            if (cleanBase.endsWith('e')) fake = cleanBase.slice(0, -1) + s;
            if (fake.toLowerCase() !== targetDeriv.toLowerCase() && fake.toLowerCase() !== cleanBase) {
                candidates.add(fake);
            }
        });

        const list = Array.from(candidates);
        return shuffle(list).slice(0, 3);
    }

    /**
     * Start a new Quiz Session
     */
    function startSession(config = {}) {
        const lang = StorageManager.getActiveLanguage();
        const fullVocab = StorageManager.getVocabulary(lang);

        let pool = [];
        if (config.overrideWords && config.overrideWords.length > 0) {
            pool = [...config.overrideWords];
        } else {
            const unit = config.unit || 'ALL';
            if (unit === 'ALL') {
                pool = [...fullVocab];
            } else {
                pool = fullVocab.filter(w => w.unit === unit);
            }
        }

        if (pool.length === 0) {
            return { success: false, message: 'No vocabulary words found for selected filter.' };
        }

        pool = shuffle(pool);

        let count = pool.length;
        if (config.count && config.count !== 'all') {
            const req = parseInt(config.count, 10);
            if (!isNaN(req) && req < pool.length) {
                count = req;
                pool = pool.slice(0, req);
            }
        }

        const stats = StorageManager.getStats(lang);

        state = {
            active: true,
            selectedType: config.type || 'mixed',
            vocabularyPool: fullVocab,
            questionQueue: pool,
            currentIndex: 0,
            totalCount: pool.length,
            score: 0,
            wrong: 0,
            streak: 0,
            bestStreak: stats.bestStreak || 0,
            answered: false,
            selectedOption: null,
            activeQuestion: null,
            history: [],
            mistakes: []
        };

        return { success: true, totalCount: state.totalCount };
    }

    /**
     * Generate Question for current index
     */
    async function getCurrentQuestion() {
        if (state.currentIndex >= state.totalCount) {
            return null;
        }

        state.answered = false;
        state.selectedOption = null;

        const targetWord = state.questionQueue[state.currentIndex];
        const allVocab = state.vocabularyPool;

        // Choose question type
        let qType = state.selectedType;
        if (qType === 'mixed') {
            const availableTypes = ['sentence', 'def_to_word', 'word_to_def', 'meaning', 'listening'];
            if (targetWord.derivatives && targetWord.derivatives.length > 0) {
                availableTypes.push('derivatives');
            }
            // Add image matching if available
            availableTypes.push('image_match');
            qType = availableTypes[Math.floor(Math.random() * availableTypes.length)];
        }

        // Gather 3 distractors
        const otherWords = allVocab.filter(w => w.word.toLowerCase() !== targetWord.word.toLowerCase());
        const sameUnit = otherWords.filter(w => w.unit === targetWord.unit);
        let distractors = [];
        if (sameUnit.length >= 3) {
            distractors = shuffle(sameUnit).slice(0, 3);
        } else {
            distractors = shuffle(otherWords).slice(0, 3);
        }

        let qData = {
            type: qType,
            target: targetWord,
            badge: '',
            instruction: '',
            promptHtml: '',
            options: [],
            correctIndex: -1,
            correctText: '',
            audioAutoPlay: null
        };

        if (qType === 'sentence') {
            qData.badge = '📝 SENTENCE FILL-IN';
            qData.instruction = 'Which word correctly completes the sentence?';
            const blanked = blankSentence(targetWord.example, targetWord.word);
            qData.promptHtml = `
                <div class="prompt-sentence">
                    "${blanked.display}"
                    <button class="prompt-audio-btn" onclick="AudioManager.speak('${targetWord.example.replace(/'/g, "\\'")}')" title="Listen to sentence">🔊</button>
                </div>
                <div class="prompt-clue-bar">
                    <span class="pos-pill">${targetWord.pos}</span>
                    <span class="clue-text">Meaning clue: <strong>${targetWord.tr}</strong></span>
                </div>
            `;
            qData.correctText = targetWord.word;
            qData.options = shuffle([
                { text: targetWord.word, isCorrect: true },
                { text: distractors[0].word, isCorrect: false },
                { text: distractors[1].word, isCorrect: false },
                { text: distractors[2].word, isCorrect: false }
            ]);
        } else if (qType === 'derivatives' && targetWord.derivatives && targetWord.derivatives.length > 0) {
            qData.badge = '🔤 WORD FORMS & DERIVATIVES';
            const firstDeriv = targetWord.derivatives[0];
            const parts = firstDeriv.split(':');
            let formName = 'derived form';
            let correctVal = firstDeriv.trim();

            if (parts.length === 2) {
                const pType = parts[0].trim();
                correctVal = parts[1].trim();
                if (pType.includes('n')) formName = 'noun (isim) form';
                else if (pType.includes('adj')) formName = 'adjective (sıfat) form';
                else if (pType.includes('adv')) formName = 'adverb (zarf) form';
                else if (pType.includes('v')) formName = 'verb (fiil) form';
                else formName = `${pType} form`;
            }

            qData.instruction = `What is the ${formName} of the word "${targetWord.word}"?`;
            qData.promptHtml = `
                <div class="prompt-word-center">
                    <div class="prompt-big-word">${targetWord.word}</div>
                    <span class="pos-pill">${targetWord.pos}</span>
                    <div class="prompt-sub-meaning">Base Meaning: "${targetWord.tr}"</div>
                </div>
            `;
            qData.correctText = correctVal;
            const fakeDistractors = generateDerivativeDistractors(targetWord.word, correctVal);
            qData.options = shuffle([
                { text: correctVal, isCorrect: true },
                { text: fakeDistractors[0] || distractors[0].word, isCorrect: false },
                { text: fakeDistractors[1] || distractors[1].word, isCorrect: false },
                { text: fakeDistractors[2] || distractors[2].word, isCorrect: false }
            ]);
        } else if (qType === 'def_to_word') {
            qData.badge = '📖 DEFINITION ➔ WORD';
            qData.instruction = 'Which academic word matches this definition?';
            qData.promptHtml = `
                <div class="prompt-sentence">
                    "${targetWord.definition}"
                </div>
                <div class="prompt-clue-bar">
                    <span class="pos-pill">${targetWord.pos}</span>
                    <span class="clue-text">Academic Unit: <strong>${targetWord.unit}</strong></span>
                </div>
            `;
            qData.correctText = targetWord.word;
            qData.options = shuffle([
                { text: targetWord.word, isCorrect: true },
                { text: distractors[0].word, isCorrect: false },
                { text: distractors[1].word, isCorrect: false },
                { text: distractors[2].word, isCorrect: false }
            ]);
        } else if (qType === 'word_to_def') {
            qData.badge = '🇬🇧 WORD ➔ DEFINITION';
            qData.instruction = `Select the accurate English definition for:`;
            qData.promptHtml = `
                <div class="prompt-word-center">
                    <div class="prompt-big-word">${targetWord.word}</div>
                    <span class="pos-pill">${targetWord.pos}</span>
                    <button class="prompt-audio-btn" onclick="AudioManager.speak('${targetWord.word.replace(/'/g, "\\'")}')" title="Listen">🔊</button>
                </div>
            `;
            qData.correctText = targetWord.definition;
            qData.options = shuffle([
                { text: targetWord.definition, isCorrect: true },
                { text: distractors[0].definition, isCorrect: false },
                { text: distractors[1].definition, isCorrect: false },
                { text: distractors[2].definition, isCorrect: false }
            ]);
            qData.audioAutoPlay = targetWord.word;
        } else if (qType === 'listening') {
            qData.badge = '🎧 LISTENING PRACTICE';
            qData.instruction = 'Listen carefully to the audio and choose the spoken word:';
            qData.promptHtml = `
                <div class="prompt-listening-card">
                    <button class="listening-play-btn" onclick="AudioManager.speak('${targetWord.word.replace(/'/g, "\\'")}', 0.85)">
                        <span class="listen-icon">🔊</span>
                        <span class="listen-label">Play Spoken Word</span>
                    </button>
                    <div class="listening-hint">Part of Speech: <strong>${targetWord.pos}</strong> &bull; Meaning: <em>${targetWord.tr}</em></div>
                </div>
            `;
            qData.correctText = targetWord.word;
            qData.options = shuffle([
                { text: targetWord.word, isCorrect: true },
                { text: distractors[0].word, isCorrect: false },
                { text: distractors[1].word, isCorrect: false },
                { text: distractors[2].word, isCorrect: false }
            ]);
            qData.audioAutoPlay = targetWord.word;
        } else if (qType === 'image_match') {
            qData.badge = '🖼️ VISUAL VOCABULARY';
            qData.instruction = 'Which academic word corresponds to this concept / image?';
            const imgUrl = targetWord.imageUrl || await DictionaryService.fetchWordImage(targetWord.word);
            qData.promptHtml = `
                <div class="prompt-image-card">
                    <img src="${imgUrl}" alt="${targetWord.word}" class="quiz-visual-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=600&q=80';" />
                    <div class="prompt-clue-bar" style="margin-top:10px;">
                        <span class="pos-pill">${targetWord.pos}</span>
                        <span class="clue-text">Context: "${blankSentence(targetWord.example, targetWord.word).display}"</span>
                    </div>
                </div>
            `;
            qData.correctText = targetWord.word;
            qData.options = shuffle([
                { text: targetWord.word, isCorrect: true },
                { text: distractors[0].word, isCorrect: false },
                { text: distractors[1].word, isCorrect: false },
                { text: distractors[2].word, isCorrect: false }
            ]);
        } else {
            // meaning
            qData.badge = '🌐 WORD ➔ TRANSLATION';
            qData.instruction = `What is the meaning of the word "${targetWord.word}"?`;
            qData.promptHtml = `
                <div class="prompt-word-center">
                    <div class="prompt-big-word">${targetWord.word}</div>
                    <span class="pos-pill">${targetWord.pos}</span>
                    <button class="prompt-audio-btn" onclick="AudioManager.speak('${targetWord.word.replace(/'/g, "\\'")}')" title="Listen">🔊</button>
                    <div class="prompt-sub-meaning">Longman Definition: "${targetWord.definition}"</div>
                </div>
            `;
            qData.correctText = targetWord.tr;
            qData.options = shuffle([
                { text: targetWord.tr, isCorrect: true },
                { text: distractors[0].tr, isCorrect: false },
                { text: distractors[1].tr, isCorrect: false },
                { text: distractors[2].tr, isCorrect: false }
            ]);
            qData.audioAutoPlay = targetWord.word;
        }

        qData.correctIndex = qData.options.findIndex(o => o.isCorrect);
        state.activeQuestion = qData;
        return qData;
    }

    /**
     * Submit an answer for the current active question
     */
    function submitAnswer(optionIndex) {
        if (!state.active || state.answered || state.activeQuestion === null) {
            return null;
        }

        state.answered = true;
        state.selectedOption = optionIndex;
        const q = state.activeQuestion;
        const isCorrect = (optionIndex === q.correctIndex);
        const lang = StorageManager.getActiveLanguage();

        if (isCorrect) {
            AudioManager.playSound('correct');
            state.score++;
            state.streak++;
            state.bestStreak = Math.max(state.bestStreak, state.streak);
            state.history.push({ word: q.target, correct: true, questionType: q.type });
        } else {
            AudioManager.playSound('wrong');
            state.wrong++;
            state.streak = 0;
            state.mistakes.push(q.target);
            state.history.push({ word: q.target, correct: false, questionType: q.type });
        }

        // Persist rolling stats
        const currentStats = StorageManager.getStats(lang);
        currentStats.totalSolved++;
        if (isCorrect) currentStats.correct++;
        else currentStats.wrong++;
        currentStats.streak = state.streak;
        currentStats.bestStreak = Math.max(currentStats.bestStreak || 0, state.bestStreak);
        currentStats.lastSessionDate = new Date().toISOString();
        StorageManager.saveStats(currentStats, lang);

        return {
            isCorrect,
            correctIndex: q.correctIndex,
            correctText: q.correctText,
            targetWord: q.target,
            highlightedExample: highlightSentence(q.target.example, q.target.word),
            score: state.score,
            streak: state.streak,
            bestStreak: state.bestStreak
        };
    }

    function nextQuestion() {
        state.currentIndex++;
        state.answered = false;
        state.selectedOption = null;
        return state.currentIndex < state.totalCount;
    }

    function getResults() {
        const total = state.totalCount;
        const correct = state.score;
        const wrong = state.wrong;
        const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0;

        return {
            total,
            correct,
            wrong,
            accuracy,
            bestStreak: state.bestStreak,
            history: state.history,
            mistakes: state.mistakes
        };
    }

    function getState() {
        return { ...state };
    }

    return {
        QUESTION_TYPES,
        startSession,
        getCurrentQuestion,
        submitAnswer,
        nextQuestion,
        getResults,
        getState,
        blankSentence,
        highlightSentence
    };
})();
