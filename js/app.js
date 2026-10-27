// js/app.js
// Main LexiFlow Application Controller

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

let currentUnitFilter = 'ALL';
let currentSearchQuery = '';
let activeTranslationsVisible = false;

function initApp() {
    initTheme();
    initLanguageSelector();
    initNavigation();
    renderVocabularyGrid();
    updateHeaderStats();
    initAddWordModal();
    initKeyboardShortcuts();
    initSpeakButtons();
    initSoundButton();
    initTranslations();
}

/**
 * Theme Manager
 */
function initTheme() {
    const saved = localStorage.getItem('lexiflow_theme') || 'light';
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        const btn = document.getElementById('themeToggleBtn');
        if (btn) btn.innerHTML = '☀️ Light';
    }
}

function toggleTheme() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const btn = document.getElementById('themeToggleBtn');
    if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('lexiflow_theme', 'light');
        if (btn) btn.innerHTML = '🌙 Dark';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('lexiflow_theme', 'dark');
        if (btn) btn.innerHTML = '☀️ Light';
    }
}

/**
 * Language Selector & Multi-Language Memory Profile
 */
function initLanguageSelector() {
    const select = document.getElementById('langSelect');
    if (!select) return;

    select.innerHTML = '';
    const langs = StorageManager.SUPPORTED_LANGUAGES;
    const active = StorageManager.getActiveLanguage();

    Object.keys(langs).forEach(code => {
        const opt = document.createElement('option');
        opt.value = code;
        opt.innerText = `${langs[code].flag} ${langs[code].name} (${langs[code].label})`;
        if (code === active) opt.selected = true;
        select.appendChild(opt);
    });

    select.addEventListener('change', (e) => {
        const newLang = e.target.value;
        StorageManager.setActiveLanguage(newLang);
        showToast(`Switched profile to ${langs[newLang].name}`);
        // A running session belongs to the previous language profile
        if (QuizEngine.getState().active) {
            QuizEngine.endSession();
            showQuizSetupScreen();
        }
        renderVocabularyGrid();
        updateHeaderStats();
        startTranslationsIfNeeded();
    });
}

/**
 * Navigation Mode Switcher
 */
function initNavigation() {
    const tabList = document.getElementById('tabList');
    const tabQuiz = document.getElementById('tabQuiz');

    if (tabList) tabList.onclick = () => switchMode('list');
    if (tabQuiz) tabQuiz.onclick = () => switchMode('quiz');
}

function switchMode(mode) {
    const tabList = document.getElementById('tabList');
    const tabQuiz = document.getElementById('tabQuiz');
    const listView = document.getElementById('listView');
    const quizView = document.getElementById('quizView');

    if (mode === 'list') {
        tabList.classList.add('active');
        tabQuiz.classList.remove('active');
        listView.style.display = 'block';
        quizView.style.display = 'none';
        document.body.classList.remove('quiz-playing');
        renderVocabularyGrid();
    } else {
        tabList.classList.remove('active');
        tabQuiz.classList.add('active');
        listView.style.display = 'none';
        quizView.style.display = 'block';
        showQuizSetupScreen();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Header Stats
 */
function updateHeaderStats() {
    const vocab = StorageManager.getVocabulary();
    const stats = StorageManager.getStats();

    const totalEl = document.getElementById('totalWordsCount');
    const badgeEl = document.getElementById('listCountBadge');
    if (totalEl) totalEl.innerText = vocab.length;
    if (badgeEl) badgeEl.innerText = vocab.length;

    const streakEl = document.getElementById('setupStreakVal');
    const totalSolvedEl = document.getElementById('setupSolvedVal');
    const accEl = document.getElementById('setupAccuracyVal');

    if (streakEl) streakEl.innerText = stats.streak || 0;
    if (totalSolvedEl) totalSolvedEl.innerText = stats.totalSolved || 0;
    const acc = stats.totalSolved > 0 ? Math.round((stats.correct / stats.totalSolved) * 100) : 0;
    if (accEl) accEl.innerText = '%' + acc;
}

/**
 * Vocabulary Cards Rendering
 */
function renderVocabularyGrid() {
    const grid = document.getElementById('vocabGrid');
    if (!grid) return;

    const vocab = StorageManager.getVocabulary();
    const query = currentSearchQuery.toLowerCase().trim();

    const filtered = vocab.filter(item => {
        const matchesUnit = (currentUnitFilter === 'ALL' || item.unit === currentUnitFilter);
        const matchesQuery = !query ||
            item.word.toLowerCase().includes(query) ||
            item.definition.toLowerCase().includes(query) ||
            item.tr.toLowerCase().includes(query) ||
            item.example.toLowerCase().includes(query);
        return matchesUnit && matchesQuery;
    });

    grid.innerHTML = '';
    if (filtered.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
                <div style="font-size: 3rem; margin-bottom: 12px;">🔍</div>
                <h3>No words found</h3>
                <p>Try adjusting your search query or unit filter, or add a new word!</p>
            </div>
        `;
        return;
    }

    filtered.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = 'vocab-card';
        card.setAttribute('data-id', item.id);

        let derivHtml = '';
        if (item.derivatives && item.derivatives.length > 0) {
            const badges = item.derivatives.map(d => `<span class="deriv-badge">${escapeHtml(d)}</span>`).join(' ');
            derivHtml = `
                <div class="deriv-row">
                    <span class="deriv-title">Forms:</span>
                    <div class="deriv-tags">${badges}</div>
                </div>
            `;
        }

        const hasTr = !!item.tr;
        const displayTr = !hasTr ? '⏳ translation pending' : (activeTranslationsVisible ? escapeHtml(item.tr) : reverseText(item.tr));
        const trClass = (activeTranslationsVisible || !hasTr) ? 'tr-content' : 'tr-content reversed';

        card.innerHTML = `
            <div class="card-top">
                <span class="card-id">#${item.id || idx + 1}</span>
                <div class="word-meta">
                    <h3 class="word-head">${escapeHtml(item.word)}</h3>
                    <span class="pos-tag">${escapeHtml(item.pos)}</span>
                </div>
                <div class="card-actions-row">
                    <button class="card-icon-btn" data-speak="${escapeHtml(item.word)}" title="Pronounce word">🔊</button>
                    <button class="card-icon-btn btn-delete" onclick="handleDeleteWord(${item.id})" title="Delete word">🗑️</button>
                </div>
            </div>

            <div class="section-tag">${escapeHtml(item.unit)} &bull; ${escapeHtml(item.section || 'General')}</div>
            <p class="definition-text">${escapeHtml(item.definition)}</p>

            <div class="example-box">
                <p class="example-text">${escapeHtml(item.example)}</p>
            </div>

            ${derivHtml}

            <div class="tr-footer">
                <span class="tr-label">Meaning:</span>
                <div class="tr-interactive" ${hasTr ? `data-tr="${escapeHtml(item.tr)}"` : ''} title="Click to flip text">
                    <span class="${trClass}">${displayTr}</span>
                    ${hasTr ? '<span class="flip-hint">⟲ flip</span>' : ''}
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

/**
 * Delegated handlers (avoid inline-JS quoting bugs with text containing quotes)
 */
function initSpeakButtons() {
    document.addEventListener('click', (e) => {
        const speakBtn = e.target.closest('[data-speak]');
        if (speakBtn) {
            AudioManager.speak(speakBtn.dataset.speak, parseFloat(speakBtn.dataset.rate) || 0.9);
            return;
        }
        const trBox = e.target.closest('.tr-interactive');
        if (trBox) toggleSingleTr(trBox);
    });
}

function initSoundButton() {
    const btn = document.getElementById('soundToggleBtn');
    if (!btn) return;
    btn.innerText = AudioManager.isSoundEnabled() ? '🔊' : '🔇';
    btn.onclick = () => {
        const on = AudioManager.toggleSound();
        btn.innerText = on ? '🔊' : '🔇';
        if (on) AudioManager.playSound('click');
    };
}

/**
 * Non-Turkish profiles: background translation with progress bar
 */
function initTranslations() {
    TranslationService.onChange((lang, progress) => {
        if (lang !== StorageManager.getActiveLanguage()) return;
        renderTranslationBar(progress);
        renderVocabularyGridThrottled();
    });
    startTranslationsIfNeeded();
}

function startTranslationsIfNeeded() {
    renderTranslationBar(TranslationService.getProgress());
    if (StorageManager.getActiveLanguage() !== 'tr') {
        TranslationService.run(StorageManager.getActiveLanguage());
    }
}

function retryTranslations() {
    TranslationService.run(StorageManager.getActiveLanguage());
}

let gridRefreshTimer = null;
function renderVocabularyGridThrottled() {
    if (gridRefreshTimer) return;
    gridRefreshTimer = setTimeout(() => {
        gridRefreshTimer = null;
        const listView = document.getElementById('listView');
        if (listView && listView.style.display !== 'none') renderVocabularyGrid();
    }, 1500);
}

function renderTranslationBar(p) {
    const bar = document.getElementById('translationBar');
    if (!bar) return;
    if (StorageManager.getActiveLanguage() === 'tr' || p.total === 0) {
        bar.style.display = 'none';
        return;
    }
    const langName = StorageManager.SUPPORTED_LANGUAGES[p.lang].label;
    const pct = Math.round((p.done / p.total) * 100);
    let text;
    if (p.running) text = `🌐 Translating to ${langName}… ${p.done} / ${p.total}`;
    else if (p.done >= p.total) text = `✅ All ${p.total} words translated to ${langName}`;
    else if (p.status === 'quota') text = `⚠️ Free translation quota reached (${p.done} / ${p.total}). Progress is saved: try again later.`;
    else if (p.status === 'offline') text = `⚠️ Could not reach the translation service (${p.done} / ${p.total}). Check your connection.`;
    else text = `🌐 ${p.done} / ${p.total} words translated to ${langName}`;

    bar.style.display = 'flex';
    document.getElementById('translationStatusText').innerText = text;
    document.getElementById('translationProgressFill').style.width = pct + '%';
    const retry = document.getElementById('translationRetryBtn');
    retry.style.display = (!p.running && p.done < p.total) ? 'inline-flex' : 'none';
}

function handleSearch(query) {
    currentSearchQuery = query;
    renderVocabularyGrid();
}

function setUnitFilter(unit, btn) {
    currentUnitFilter = unit;
    document.querySelectorAll('.unit-pill').forEach(p => p.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderVocabularyGrid();
}

function toggleSingleTr(container) {
    const normalTr = container.dataset.tr;
    if (!normalTr) return;
    const textEl = container.querySelector('.tr-content');
    const hintEl = container.querySelector('.flip-hint');

    if (textEl.classList.contains('reversed')) {
        textEl.innerText = normalTr;
        textEl.classList.remove('reversed');
        hintEl.innerText = '⟲ hide';
    } else {
        textEl.innerText = reverseText(normalTr);
        textEl.classList.add('reversed');
        hintEl.innerText = '⟲ flip';
    }
}

function toggleAllTranslations() {
    activeTranslationsVisible = !activeTranslationsVisible;
    const btn = document.getElementById('toggleTrBtn');
    if (btn) {
        btn.innerText = activeTranslationsVisible ? '🔄 Hide Meanings (Self-Test)' : '🔄 Show All Meanings';
    }
    renderVocabularyGrid();
}

function reverseText(str) {
    if (!str) return '';
    return str.split('').reverse().join('');
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Add / Manage Words Modal & Auto-Dictionary
 */
function initAddWordModal() {
    const modal = document.getElementById('addWordModal');
    const openBtn = document.getElementById('openAddWordBtn');
    const closeBtn = document.getElementById('closeAddWordBtn');
    const cancelBtn = document.getElementById('cancelAddWordBtn');
    const autoFetchBtn = document.getElementById('autoFetchBtn');
    const form = document.getElementById('addWordForm');

    if (openBtn) openBtn.onclick = () => openModal();
    if (closeBtn) closeBtn.onclick = () => closeModal();
    if (cancelBtn) cancelBtn.onclick = () => closeModal();

    if (autoFetchBtn) {
        autoFetchBtn.onclick = async () => {
            const wordInput = document.getElementById('newWordInput');
            const word = wordInput.value.trim();
            if (!word) {
                showToast('Please type a word first to fetch.');
                wordInput.focus();
                return;
            }

            autoFetchBtn.disabled = true;
            autoFetchBtn.innerText = '⏳ Looking up...';

            try {
                const lang = StorageManager.getActiveLanguage();
                const dictPromise = DictionaryService.lookupEnglishWord(word);
                const transPromise = DictionaryService.translateWord(word, lang);

                const [dictData, translation] = await Promise.all([dictPromise, transPromise]);

                if (dictData) {
                    if (dictData.pos) document.getElementById('newWordPos').value = dictData.pos;
                    if (dictData.definition) document.getElementById('newWordDef').value = dictData.definition;
                    if (dictData.example) document.getElementById('newWordExample').value = dictData.example;
                    if (dictData.derivatives && dictData.derivatives.length > 0) {
                        document.getElementById('newWordDeriv').value = dictData.derivatives.join(', ');
                    }
                }

                if (translation) {
                    document.getElementById('newWordTr').value = translation;
                }

                showToast('✓ Dictionary definition and translation fetched!');
            } catch (err) {
                showToast('Failed to auto-fetch. You can type details manually.');
            } finally {
                autoFetchBtn.disabled = false;
                autoFetchBtn.innerText = '🔍 Auto-Fetch Dictionary';
            }
        };
    }

    if (form) {
        form.onsubmit = (e) => {
            e.preventDefault();
            const word = document.getElementById('newWordInput').value.trim();
            if (!word) return;

            const pos = document.getElementById('newWordPos').value;
            const unit = document.getElementById('newWordUnit').value;
            const def = document.getElementById('newWordDef').value.trim();
            const ex = document.getElementById('newWordExample').value.trim();
            const tr = document.getElementById('newWordTr').value.trim();
            const rawDeriv = document.getElementById('newWordDeriv').value.trim();
            const derivatives = rawDeriv ? rawDeriv.split(',').map(s => s.trim()).filter(Boolean) : [];

            StorageManager.addWord({
                word,
                pos,
                unit,
                definition: def || 'Academic concept',
                example: ex || `The concept of ${word} is widely discussed.`,
                tr: tr || word,
                derivatives
            });

            closeModal();
            form.reset();
            renderVocabularyGrid();
            updateHeaderStats();
            showToast(`Added "${word}" to vocabulary!`);
        };
    }

    function openModal() {
        modal.classList.add('active');
        document.body.classList.add('modal-open');
        // Do not pop the on-screen keyboard open on touch devices
        if (!window.matchMedia('(pointer: coarse)').matches) {
            document.getElementById('newWordInput').focus();
        }
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.classList.remove('modal-open');
    }

    // Tap on the dimmed backdrop or press Escape to close
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) closeModal();
        });
    }
}

function handleDeleteWord(wordId) {
    if (confirm('Are you sure you want to delete this word from the vocabulary?')) {
        StorageManager.deleteWord(wordId);
        renderVocabularyGrid();
        updateHeaderStats();
        showToast('Word deleted from vocabulary.');
    }
}

function handleResetVocabulary() {
    if (confirm('Reset vocabulary to the default word list? Custom words you added will be removed.')) {
        StorageManager.resetVocabulary();
        renderVocabularyGrid();
        updateHeaderStats();
        showToast('Vocabulary reset to default word list.');
        startTranslationsIfNeeded();
    }
}

function handleExportJSON() {
    const jsonStr = StorageManager.exportJSON();
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lexiflow_vocab_${StorageManager.getActiveLanguage()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Vocabulary exported as JSON!');
}

/**
 * Toast Notifications
 */
function showToast(message) {
    let toast = document.getElementById('toastNotice');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toastNotice';
        toast.className = 'toast-notice';
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 2800);
}

/**
 * DUOLINGO PRACTICE LAB CONTROLLER
 */
function showQuizSetupScreen() {
    document.body.classList.remove('quiz-playing');
    document.getElementById('quizSetupScreen').style.display = 'block';
    document.getElementById('quizPlayScreen').style.display = 'none';
    document.getElementById('quizResultScreen').style.display = 'none';
    updateHeaderStats();
}

function startQuizFromSetup() {
    const unit = document.getElementById('quizSetupUnitSelect').value;
    const type = document.getElementById('quizSetupTypeSelect').value;
    const count = document.getElementById('quizSetupCountSelect').value;

    const res = QuizEngine.startSession({ unit, type, count });
    if (!res.success) {
        alert(res.message);
        return;
    }

    document.getElementById('quizSetupScreen').style.display = 'none';
    document.getElementById('quizResultScreen').style.display = 'none';
    document.getElementById('quizPlayScreen').style.display = 'block';
    document.body.classList.add('quiz-playing');

    renderQuizQuestion();
}

async function renderQuizQuestion() {
    const qData = await QuizEngine.getCurrentQuestion();
    if (!qData) {
        showQuizResultsScreen();
        return;
    }

    const qState = QuizEngine.getState();
    const curIdx = qState.currentIndex;
    const total = qState.totalCount;

    // Progress bar & counters
    const pct = (curIdx / total) * 100;
    document.getElementById('quizProgressFill').style.width = `${pct}%`;
    document.getElementById('quizStreakVal').innerText = qState.streak;
    document.getElementById('quizCounterVal').innerText = `${curIdx + 1} / ${total}`;

    // Meta & Instructions
    document.getElementById('questionTypeBadge').innerText = qData.badge;
    document.getElementById('questionUnitTag').innerText = `${qData.target.unit} • ${qData.target.section || 'Vocab'}`;
    document.getElementById('questionInstruction').innerText = qData.instruction;
    document.getElementById('questionPromptCard').innerHTML = qData.promptHtml;

    // Options Grid
    const optGrid = document.getElementById('quizOptionsGrid');
    optGrid.innerHTML = '';
    qData.options.forEach((opt, idx) => {
        const btn = document.createElement('div');
        btn.className = 'duo-option';
        btn.id = `duoOpt_${idx}`;
        btn.onclick = () => selectQuizOption(idx);
        btn.ondblclick = () => {
            selectQuizOption(idx);
            submitQuizAnswer();
        };
        btn.innerHTML = `
            <div class="option-key-badge">${idx + 1}</div>
            <div class="option-label-text">${escapeHtml(opt.text)}</div>
        `;
        optGrid.appendChild(btn);
    });

    // Reset Bottom Sheet
    const sheet = document.getElementById('quizBottomSheet');
    sheet.className = 'duo-bottom-sheet state-default';
    sheet.innerHTML = `
        <button class="duo-btn duo-btn-primary duo-btn-lg" id="quizCheckBtn" onclick="submitQuizAnswer()" disabled>
            CHECK
        </button>
    `;

    // On phones a new question can be shorter than the previous one: start at its top
    if (window.matchMedia('(max-width: 639px)').matches) {
        const playScreen = document.getElementById('quizPlayScreen');
        if (playScreen) playScreen.scrollIntoView({ block: 'start', behavior: 'smooth' });
    }

    // Auto-play audio if applicable
    if (qData.audioAutoPlay && AudioManager.isSoundEnabled()) {
        setTimeout(() => AudioManager.speak(qData.audioAutoPlay), 200);
    }
}

function selectQuizOption(index) {
    const qState = QuizEngine.getState();
    if (qState.answered) return;

    AudioManager.playSound('click');
    document.querySelectorAll('.duo-option').forEach((el, idx) => {
        el.classList.toggle('selected', idx === index);
    });

    const checkBtn = document.getElementById('quizCheckBtn');
    if (checkBtn) {
        checkBtn.disabled = false;
        checkBtn.classList.remove('duo-btn-disabled');
    }
}

function submitQuizAnswer() {
    const qState = QuizEngine.getState();
    if (qState.answered) return;

    const selectedIndex = Array.from(document.querySelectorAll('.duo-option')).findIndex(el => el.classList.contains('selected'));
    if (selectedIndex === -1) return;

    const result = QuizEngine.submitAnswer(selectedIndex);
    if (!result) return;

    document.querySelectorAll('.duo-option').forEach(el => el.classList.add('disabled'));
    const selectedEl = document.getElementById(`duoOpt_${selectedIndex}`);
    const correctEl = document.getElementById(`duoOpt_${result.correctIndex}`);
    const sheet = document.getElementById('quizBottomSheet');

    if (result.isCorrect) {
        if (selectedEl) selectedEl.classList.add('option-correct');
        sheet.className = 'duo-bottom-sheet state-correct';
        sheet.innerHTML = `
            <div class="feedback-content-row">
                <div class="feedback-main-info">
                    <div class="feedback-status-icon">✓</div>
                    <div class="feedback-text-group">
                        <h3>Awesome! Correct Answer</h3>
                        <div class="feedback-card-detail">
                            <strong>${escapeHtml(result.targetWord.word)}</strong> <span style="color:var(--accent-pos)">${escapeHtml(result.targetWord.pos)}</span>${result.targetWord.tr ? ` &bull; <span>${escapeHtml(result.targetWord.tr)}</span>` : ''}
                            <div class="detail-sentence">"${result.highlightedExample}"</div>
                        </div>
                    </div>
                </div>
                <div class="feedback-actions">
                    <button class="duo-icon-btn" data-speak="${escapeHtml(result.targetWord.word)}" title="Pronounce">🔊</button>
                    <button class="duo-btn duo-btn-primary duo-btn-lg" onclick="advanceNextQuizQuestion()">CONTINUE ➔</button>
                </div>
            </div>
        `;
    } else {
        if (selectedEl) selectedEl.classList.add('option-wrong');
        if (correctEl) correctEl.classList.add('option-correct');
        sheet.className = 'duo-bottom-sheet state-wrong';
        sheet.innerHTML = `
            <div class="feedback-content-row">
                <div class="feedback-main-info">
                    <div class="feedback-status-icon">✕</div>
                    <div class="feedback-text-group">
                        <h3>Incorrect!</h3>
                        <div class="correct-answer-banner">Correct Answer: <strong>${escapeHtml(result.correctText)}</strong></div>
                        <div class="feedback-card-detail">
                            <div><strong>${escapeHtml(result.targetWord.word)}</strong> <span style="color:var(--accent-pos)">${escapeHtml(result.targetWord.pos)}</span>${result.targetWord.tr ? ` &bull; <span>${escapeHtml(result.targetWord.tr)}</span>` : ''}</div>
                            <div style="margin-top:4px; font-size:0.88rem; color:var(--text-muted)"><strong>Definition:</strong> ${escapeHtml(result.targetWord.definition)}</div>
                            <div class="detail-sentence"><strong>Example:</strong> "${result.highlightedExample}"</div>
                            <div style="margin-top:6px; font-size:0.8rem; opacity:0.85;">💡 Added to your mistake review queue for focused practice.</div>
                        </div>
                    </div>
                </div>
                <div class="feedback-actions">
                    <button class="duo-icon-btn" data-speak="${escapeHtml(result.targetWord.word)}" title="Pronounce">🔊</button>
                    <button class="duo-btn duo-btn-danger duo-btn-lg" onclick="advanceNextQuizQuestion()">GOT IT, CONTINUE ➔</button>
                </div>
            </div>
        `;
    }
}

function advanceNextQuizQuestion() {
    const hasMore = QuizEngine.nextQuestion();
    if (hasMore) {
        renderQuizQuestion();
    } else {
        showQuizResultsScreen();
    }
}

function showQuizResultsScreen() {
    AudioManager.playSound('fanfare');
    document.body.classList.remove('quiz-playing');
    document.getElementById('quizPlayScreen').style.display = 'none';
    document.getElementById('quizResultScreen').style.display = 'block';

    const res = QuizEngine.getResults();

    document.getElementById('resCorrectVal').innerText = res.correct;
    document.getElementById('resWrongVal').innerText = res.wrong;
    document.getElementById('resAccuracyVal').innerText = `%${res.accuracy}`;
    document.getElementById('resBestStreakVal').innerText = `🔥 ${res.bestStreak}`;
    document.getElementById('resTotalBadge').innerText = `${res.total} Words`;

    const heading = document.getElementById('resultsTitle');
    const sub = document.getElementById('resultsSubtitle');
    if (res.accuracy >= 80) {
        heading.innerText = '🎉 Outstanding Performance!';
        sub.innerText = 'You demonstrated stellar mastery over these academic vocabulary items.';
    } else if (res.accuracy >= 50) {
        heading.innerText = '👏 Well Done! Solid Progress!';
        sub.innerText = 'You are on the right track. Practice your missed words to master them.';
    } else {
        heading.innerText = '💪 Good Effort! Keep Practicing!';
        sub.innerText = 'Repetition is the key to vocabulary retention. Re-drill your mistakes below.';
    }

    const repeatBtn = document.getElementById('repeatMistakesBtn');
    const mistakeCountSpan = document.getElementById('mistakeCountSpan');
    if (res.mistakes.length > 0) {
        repeatBtn.style.display = 'inline-flex';
        mistakeCountSpan.innerText = res.mistakes.length;
    } else {
        repeatBtn.style.display = 'none';
    }

    const container = document.getElementById('resWordsContainer');
    container.innerHTML = '';
    res.history.forEach(item => {
        const row = document.createElement('div');
        row.className = 'results-word-item';
        row.innerHTML = `
            <div class="res-word-left">
                <span class="res-word-tag ${item.correct ? 'tag-correct' : 'tag-wrong'}">
                    ${item.correct ? '✓ Correct' : '✕ Mistake'}
                </span>
                <div>
                    <span class="res-word-title">${escapeHtml(item.word.word)}</span>
                    <span style="font-size:0.8rem; color:var(--accent-pos)">${escapeHtml(item.word.pos)}</span>
                    <div class="res-word-tr">${item.word.tr ? escapeHtml(item.word.tr) + ' &bull; ' : ''}<em style="font-size:0.8rem">"${escapeHtml(item.word.example)}"</em></div>
                </div>
            </div>
            <button class="duo-icon-btn" data-speak="${escapeHtml(item.word.word)}" title="Pronounce">🔊</button>
        `;
        container.appendChild(row);
    });

    updateHeaderStats();
}

function handleRepeatMistakes() {
    const res = QuizEngine.getResults();
    if (res.mistakes.length === 0) return;

    QuizEngine.startSession({ overrideWords: res.mistakes });
    document.getElementById('quizResultScreen').style.display = 'none';
    document.getElementById('quizPlayScreen').style.display = 'block';
    document.body.classList.add('quiz-playing');
    renderQuizQuestion();
}

function confirmQuitQuiz() {
    if (confirm('Are you sure you want to exit the practice session?')) {
        showQuizSetupScreen();
    }
}

/**
 * Keyboard Controls (1-4, Enter, Space)
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        const playScreen = document.getElementById('quizPlayScreen');
        if (playScreen && playScreen.style.display !== 'none') {
            if (['1', '2', '3', '4'].includes(e.key)) {
                const idx = parseInt(e.key, 10) - 1;
                selectQuizOption(idx);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                const qState = QuizEngine.getState();
                if (!qState.answered) {
                    submitQuizAnswer();
                } else {
                    advanceNextQuizQuestion();
                }
            } else if (e.key === ' ' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                const qState = QuizEngine.getState();
                if (qState.activeQuestion) {
                    AudioManager.speak(qState.activeQuestion.target.word);
                }
            }
        }
    });
}
