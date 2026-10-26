<div align="center">

# 🦉 LexiFlow

**Interactive Academic English Vocabulary & Gamified Learning Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-brightgreen.svg)]()
[![Offline First](https://img.shields.io/badge/Offline-Ready-success.svg)]()

<p align="center">
  A sleek, modular, zero-dependency academic English vocabulary platform built with pure HTML5, CSS3, and modern JavaScript. Features a Duolingo-style practice lab, audio pronunciation, word form derivations, smart dictionary auto-fetch, and multi-language memory profiles.
</p>

[Key Features](#-key-features) •
[Quick Start](#-quick-start) •
[Practice Modes](#-practice-modes-quiz-lab) •
[Architecture](#-modular-architecture) •
[Keyboard Shortcuts](#-keyboard-shortcuts) •
[License](#-license)

---

</div>

## 🌟 Key Features

### 🦉 Duolingo-Inspired Practice Lab
- **Gamified Feedback**: Animated green progress bar, streak flame counter (`🔥`), accuracy rate, and instant tactile 3D buttons.
- **Synthesized Audio Effects**: 100% offline, zero-latency Web Audio API chords for correct answers, wrong buzzers, button clicks, and completion fanfares.
- **Mistake Learning Loop**: Incorrect answers immediately reveal the correct word, its part of speech, Longman definition, translation, and sentence with highlighted context. Missed words are automatically added to a review queue with a 1-click **"🔁 Practice Mistakes Only"** drill.

### 📚 Rich Question Diversity
1. **🔤 Word Forms & Derivatives**: Practice secondary forms (noun, verb, adjective, adverb derivations e.g., *analyze* ➔ *analysis*, *create* ➔ *creative*).
2. **📝 Sentence Fill-in**: Identify missing words in Longman contextual academic sentences.
3. **🎧 Listening Drill**: Audio pronunciation challenge — listen to spoken English and select the matching word.
4. **🖼️ Visual Vocabulary**: Match images and visual concepts to their corresponding academic terms.
5. **📖 English Definitions**: Match words to Longman academic definitions and vice versa.
6. **🌐 Multi-Language Translations**: Test word meanings against your active target language.

### 🔍 Smart Dictionary Assistant (Auto-Fetch & Auto-Fill)
- Adding new words is effortless: type any English word (e.g. *resilient*, *innovate*, *sustainability*) and click **"🔍 Auto-Fetch Dictionary"**.
- The system automatically queries public dictionary and translation APIs to populate:
  - Part of Speech (`(n)`, `(v)`, `(adj)`, `(adv)`)
  - Precise academic definition
  - Authentic example sentence
  - Derived forms and synonyms
  - Target language translation
- Full CRUD: Add custom words, delete words, export/import JSON, or reset to the default 520 curated words anytime.

### 🌐 Multi-Language Profiles with Isolated Memory
- Switch between different language profiles:
  - 🇹🇷 **Turkish** (Türkçe)
  - 🇪🇸 **Spanish** (Español)
  - 🇩🇪 **German** (Deutsch)
  - 🇫🇷 **French** (Français)
  - 🇮🇹 **Italian** (Italiano)
  - 🇸🇦 **Arabic** (العربية)
- Each language profile maintains its own independent `localStorage` namespace for statistics, streaks, solved counts, custom words, and review queues.

### 🔊 Native Speech Synthesis
- Pronounce any word or contextual sentence anytime with a click (🔊) using the browser's native **Web Speech API** (`en-US`).

### 🌓 Modern Design & Accessibility
- Clean **Light** and **Dark** themes.
- Responsive design tailored for mobile phones, tablets, and desktops.
- Quick-flip cards for self-study and flashcard memorization.
- Print-friendly layout for creating physical paper study sheets.

---

## 🚀 Quick Start

No installations, build tools, or server environments are required.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/lexiflow.git
cd lexiflow
```

### 2. Run the application
Simply double-click or open **`index.html`** in any modern web browser (Chrome, Firefox, Safari, Edge, Brave):
```bash
# On Linux
xdg-open index.html

# On macOS
open index.html

# On Windows
start index.html
```

Or deploy directly to **GitHub Pages**, **Vercel**, or **Netlify** with zero configuration.

---

## 🎯 Practice Modes (Quiz Lab)

| Question Mode | Description | Educational Focus |
|---|---|---|
| **🔀 Mixed Mode** | Seamlessly alternates across all question types | Comprehensive test preparation |
| **🔤 Derivatives** | Tests secondary forms (Noun / Verb / Adj / Adv) | Morphological mastery |
| **📝 Sentence Fill-in** | Replaces target word with a blank (`__________`) | Contextual and reading usage |
| **🎧 Listening Drill** | Spoken audio prompt with hidden word text | Listening comprehension & phonetics |
| **🖼️ Visual Match** | Visual image / concept card matching | Associative visual memory |
| **📖 Definition ➔ Word** | Given academic definition, choose target word | Reading & vocabulary recall |
| **🇬🇧 Word ➔ Definition** | Given academic word, choose correct definition | Definition comprehension |
| **🌐 Word ➔ Translation** | Given word, choose meaning in active language | Translation & bilingual fluency |

---

## 🏗️ Modular Architecture

```
lexiflow/
├── index.html               # Main application entry point (clean & semantic HTML5)
├── css/
│   ├── styles.css           # Global layout, themes, typography & card styles
│   └── quiz.css             # Duolingo-style game UI, animations & feedback drawer
├── js/
│   ├── default-data.js      # Built-in 520 curated academic words across 10 units
│   ├── storage.js           # Multi-language memory manager & localStorage CRUD
│   ├── dictionary-api.js    # Smart auto-lookup for definitions, audio, images & translation
│   ├── speech.js            # Web Speech API TTS & Web Audio game sound synthesizer
│   ├── quiz-engine.js       # Game loop, question generators, streak & mistake review
│   └── app.js               # Application router, UI listeners & keyboard controller
├── data/
│   └── vocabulary.json      # Standalone JSON export of the complete lexicon
├── dist/
│   └── standalone.html      # Optional single-file offline compilation
├── vocabulary_guide.md      # Printable markdown study guide
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## ⌨️ Keyboard Shortcuts

Speed up your practice sessions with intuitive keyboard shortcuts:

| Key | Action |
|---|---|
| `1`, `2`, `3`, `4` | Select option 1, 2, 3, or 4 |
| `Enter` | Check answer / Advance to next question |
| `Space` | Replay spoken audio pronunciation |
| `Esc` | Close open modals or dialogs |

---

## 🤝 Contributing

Contributions, feedback, and suggestions are warmly welcomed!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
