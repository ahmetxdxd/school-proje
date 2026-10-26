import sys
import os
import html
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from unit01 import get_unit_1
from unit02 import get_unit_2
from unit03 import get_unit_3
from unit04 import get_unit_4
from unit05 import get_unit_5
from unit06 import get_unit_6
from unit07 import get_unit_7
from unit08 import get_unit_8
from unit09 import get_unit_9
from unit10 import get_unit_10

units_data = {
    "Unit 1: Social Relationships & Shopping Psychology": get_unit_1(),
    "Unit 2: It's In My DNA & Science and Investigation": get_unit_2(),
    "Unit 3: City Solutions & On the Move": get_unit_3(),
    "Unit 4: Danger Zones & People and the Planet": get_unit_4(),
    "Unit 5: The Travel Business & Rise to the Top": get_unit_5(),
    "Unit 6: Product Design & Design with Purpose": get_unit_6(),
    "Unit 7: Global Challenges & Inspired to Protect": get_unit_7(),
    "Unit 8: Medical Innovations & Traditional and Modern Medicine": get_unit_8(),
    "Unit 9: Languages and Culture & Uncovering the Past": get_unit_9(),
    "Unit 10: Survival Instinct & Feelings & Emotions": get_unit_10(),
}

def reverse_tr(text):
    return text[::-1]

total_words = sum(len(w_list) for w_list in units_data.values())
print(f"Compiling {total_words} words across {len(units_data)} units...")

# ==========================================
# 1. GENERATE MARKDOWN
# ==========================================
md_lines = [
    "# Kadir Has Üniversitesi Hazırlık Yılı Kelime Rehberi (Track 3)",
    "## Track 3 Academic Vocabulary Master Study Guide (Longman Definitions & Examples)",
    "",
    f"> **Toplam Kelime Sayısı:** {total_words} Kelime (10 Ünite Tam Liste)  ",
    "> **Format:** **Kelime** *(Tür)* &bull; Longman İngilizce Tanım &bull; Örnek Cümle &bull; Diğer Biçimler (İsim/Fiil/Sıfat/Zarf) &bull; **Ters Yazılmış Türkçe Anlam**  ",
    "> **İpucu:** Türkçe anlamlar özellikle **ters yazılmıştır** (`ikşili ,ğab` = bağ, ilişki). Böylece kendinizi test ederken gözünüz doğrudan cevaba kaymaz; sağdan sola okuyarak veya aynadan bakarak anlamı kontrol edebilirsiniz.",
    "",
    "---",
    ""
]

global_idx = 1
for unit_title, words in units_data.items():
    md_lines.append(f"## {unit_title}")
    md_lines.append("")
    
    # Group by section
    sections = {}
    for w in words:
        sec = w.get("section", "General")
        sections.setdefault(sec, []).append(w)
        
    for sec_name, sec_words in sections.items():
        md_lines.append(f"### ❖ {sec_name}")
        md_lines.append("")
        for w in sec_words:
            word = w["word"]
            pos = w["pos"]
            definition = w["definition"]
            example = w["example"]
            derivatives = w.get("derivatives", [])
            tr_normal = w["tr"]
            tr_rev = reverse_tr(tr_normal)
            
            deriv_str = ""
            if derivatives:
                deriv_lines = "<br>&nbsp;&nbsp;".join([f"• <code>{d}</code>" for d in derivatives])
                deriv_str = f"\n  - <sub>**Diğer Haller (Kelime Ailesi):**<br>&nbsp;&nbsp;{deriv_lines}</sub>"
            
            md_lines.append(f"{global_idx}. **{word}** *{pos}*")
            md_lines.append(f"  - **Tanım:** {definition}")
            md_lines.append(f"  - **Örnek:** *\"{example}\"*")
            if deriv_str:
                md_lines.append(f"  {deriv_str}")
            md_lines.append(f"  - **Türkçe (Ters):** `‹ {tr_rev} ›`")
            md_lines.append("")
            global_idx += 1
            
    md_lines.append("---")
    md_lines.append("")

md_content = "\n".join(md_lines)

# Write Markdown to workspace
with open(os.path.join(base_dir, "vocabulary_guide.md"), "w", encoding="utf-8") as f:
    f.write(md_content)

print("Markdown files generated successfully.")

# ==========================================
# 2. GENERATE RICH INTERACTIVE HTML
# ==========================================

html_cards = []
vocab_json_list = []
card_idx = 1
for unit_title, words in units_data.items():
    unit_num = unit_title.split(":")[0].strip()
    for w in words:
        word = html.escape(w["word"])
        pos = html.escape(w["pos"])
        sec = html.escape(w.get("section", ""))
        definition = html.escape(w["definition"])
        example = html.escape(w["example"])
        tr_normal = w["tr"]
        tr_rev = reverse_tr(tr_normal)
        
        deriv_html = ""
        if w.get("derivatives"):
            items = []
            for d in w["derivatives"]:
                parts = d.split(":", 1)
                if len(parts) == 2:
                    p_type = html.escape(parts[0].strip())
                    p_val = html.escape(parts[1].strip())
                    items.append(f'<span class="deriv-badge"><span class="d-type">{p_type}:</span> {p_val}</span>')
                else:
                    items.append(f'<span class="deriv-badge">{html.escape(d)}</span>')
            deriv_html = f'''
            <div class="deriv-row">
                <span class="deriv-title">Diğer Haller:</span>
                <div class="deriv-tags">{" ".join(items)}</div>
            </div>
            '''
            
        vocab_json_list.append({
            "id": card_idx,
            "unit": unit_num,
            "unitTitle": unit_title,
            "section": w.get("section", ""),
            "word": w["word"],
            "pos": w["pos"],
            "definition": w["definition"],
            "example": w["example"],
            "tr": w["tr"],
            "derivatives": w.get("derivatives", [])
        })

        html_cards.append(f'''
        <div class="vocab-card" data-unit="{html.escape(unit_num)}" data-section="{sec}" data-word="{word.lower()}" data-tr="{html.escape(tr_normal.lower())}">
            <div class="card-top">
                <span class="card-id">#{card_idx}</span>
                <div class="word-meta">
                    <h3 class="word-head">{word}</h3>
                    <span class="pos-tag">{pos}</span>
                </div>
                <span class="section-tag">{html.escape(unit_num)} &bull; {sec}</span>
            </div>
            
            <p class="definition-text">{definition}</p>
            
            <div class="example-box">
                <span class="ex-icon">❝</span>
                <p class="example-text">{example}</p>
            </div>
            
            {deriv_html}
            
            <div class="tr-footer">
                <span class="tr-label">Türkçe:</span>
                <div class="tr-interactive" onclick="toggleCardTr(this)" title="Düz / Ters metin arasında geçiş yapmak için tıklayın">
                    <span class="tr-content reversed">{html.escape(tr_rev)}</span>
                    <span class="flip-hint">⟲ çevir</span>
                </div>
            </div>
        </div>
        ''')
        card_idx += 1

html_cards_str = "\n".join(html_cards)
vocab_json_str = json.dumps(vocab_json_list, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kadir Has Hazırlık Yılı Kelime Rehberi | Track 3 Master Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border-card: #e2e8f0;
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --accent-pos: #7c3aed;
            --accent-pos-bg: #f5f3ff;
            --tr-bg: #fef2f2;
            --tr-border: #fecaca;
            --tr-text: #b91c1c;
            --radius-card: 14px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
            --shadow-hover: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
        }}

        [data-theme="dark"] {{
            --bg-body: #090d16;
            --bg-card: #131b2e;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border-card: #1e293b;
            --primary: #38bdf8;
            --primary-light: #082f49;
            --accent-pos: #a78bfa;
            --accent-pos-bg: #2e1065;
            --tr-bg: #450a0a;
            --tr-border: #7f1d1d;
            --tr-text: #fca5a5;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
            --shadow-hover: 0 10px 20px rgba(0,0,0,0.5);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.5;
            padding: 24px 16px 80px;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 32px 28px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }}

        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #2563eb, #8b5cf6, #ec4899);
        }}

        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .title-group h1 {{
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: var(--text-main);
            margin-bottom: 6px;
        }}

        .title-group p {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn {{
            appearance: none;
            border: 1px solid var(--border-card);
            background: var(--bg-card);
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 10px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
            box-shadow: var(--shadow-sm);
        }}

        .btn:hover {{
            background: var(--primary-light);
            border-color: var(--primary);
            color: var(--primary);
        }}

        .btn-primary {{
            background: var(--primary);
            color: #ffffff !important;
            border-color: var(--primary);
        }}

        .btn-primary:hover {{
            opacity: 0.92;
            transform: translateY(-1px);
        }}

        .stats-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border-card);
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .stat-item strong {{
            color: var(--text-main);
            font-weight: 700;
        }}

        /* Control Panel */
        .controls-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}

        .search-box {{
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .search-input {{
            flex: 1;
            font-family: inherit;
            font-size: 0.95rem;
            padding: 12px 18px;
            border-radius: 12px;
            border: 1.5px solid var(--border-card);
            background: var(--bg-body);
            color: var(--text-main);
            outline: none;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }}

        .search-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .unit-filter {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .unit-pill {{
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid var(--border-card);
            background: var(--bg-card);
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .unit-pill:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}

        .unit-pill.active {{
            background: var(--primary);
            border-color: var(--primary);
            color: #ffffff;
        }}

        /* Vocabulary Cards Grid */
        .vocab-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 18px;
        }}

        .vocab-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
            position: relative;
        }}

        .vocab-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: #cbd5e1;
        }}

        [data-theme="dark"] .vocab-card:hover {{
            border-color: #334155;
        }}

        .card-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}

        .card-id {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .word-meta {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            flex: 1;
        }}

        .word-head {{
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }}

        .pos-tag {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--accent-pos);
            background: var(--accent-pos-bg);
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .section-tag {{
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            background: var(--bg-body);
            padding: 3px 8px;
            border-radius: 6px;
            white-space: nowrap;
        }}

        .definition-text {{
            font-size: 0.92rem;
            color: var(--text-main);
            font-weight: 500;
            line-height: 1.45;
        }}

        .example-box {{
            background: var(--bg-body);
            border-left: 3px solid var(--primary);
            border-radius: 0 8px 8px 0;
            padding: 10px 12px;
            display: flex;
            gap: 8px;
            align-items: flex-start;
        }}

        .ex-icon {{
            font-size: 1.1rem;
            line-height: 1;
            color: var(--primary);
            opacity: 0.7;
        }}

        .example-text {{
            font-size: 0.86rem;
            color: var(--text-muted);
            font-style: italic;
            line-height: 1.42;
        }}

        /* Derivatives */
        .deriv-row {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            background: var(--bg-body);
            border-radius: 8px;
            padding: 8px 10px;
        }}

        .deriv-title {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--text-muted);
        }}

        .deriv-tags {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .deriv-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.73rem;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            padding: 2px 8px;
            border-radius: 5px;
            color: var(--text-main);
            display: inline-block;
            width: fit-content;
        }}

        .deriv-badge .d-type {{
            color: var(--primary);
            font-weight: 700;
        }}

        /* Turkish Interactive Box */
        .tr-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 10px;
            border-top: 1px dashed var(--border-card);
            margin-top: auto;
        }}

        .tr-label {{
            font-size: 0.76rem;
            font-weight: 700;
            color: var(--text-muted);
        }}

        .tr-interactive {{
            background: var(--tr-bg);
            border: 1px solid var(--tr-border);
            border-radius: 8px;
            padding: 5px 10px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s ease;
            user-select: none;
        }}

        .tr-interactive:hover {{
            opacity: 0.88;
            transform: scale(1.02);
        }}

        .tr-content {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--tr-text);
            letter-spacing: 0.02em;
        }}

        .flip-hint {{
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--tr-text);
            opacity: 0.7;
        }}

        /* Print Styles */
        @page {{
            size: A4 portrait;
            margin: 6mm 6mm 6mm 6mm;
        }}

        @media print {{
            body {{
                background: #ffffff !important;
                color: #000000 !important;
                padding: 0 !important;
                font-size: 8pt !important;
            }}

            header, .controls-card, .btn, .flip-hint, .card-id {{
                display: none !important;
            }}

            .print-header {{
                display: block !important;
                margin-bottom: 6px !important;
                padding-bottom: 3px !important;
                border-bottom: 1.5px solid #000000 !important;
            }}

            .print-header h1 {{
                font-size: 10.5pt !important;
                font-weight: 800 !important;
                margin-bottom: 1px !important;
            }}

            .print-header p {{
                font-size: 6.8pt !important;
                color: #555 !important;
            }}

            /* Default: 3 Columns for maximum space saving */
            .vocab-grid {{
                display: grid !important;
                grid-template-columns: repeat(3, 1fr) !important;
                gap: 4px !important;
            }}

            /* 2 Columns mode if chosen by user */
            body.print-2col .vocab-grid {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 5px !important;
            }}

            .vocab-card {{
                box-shadow: none !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 4px !important;
                padding: 4px 6px !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                gap: 2px !important;
            }}

            .card-top {{
                margin-bottom: 1px !important;
                gap: 4px !important;
            }}

            .word-head {{
                font-size: 8.8pt !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
            }}

            .pos-tag {{
                font-size: 6.4pt !important;
                border: 1px solid #cbd5e1 !important;
                background: #f1f5f9 !important;
                color: #4338ca !important;
                padding: 1px 3px !important;
                border-radius: 3px !important;
            }}

            .section-tag {{
                font-size: 5.6pt !important;
                padding: 1px 3px !important;
                background: #f8fafc !important;
            }}

            .definition-text {{
                font-size: 7.1pt !important;
                line-height: 1.2 !important;
                color: #0f172a !important;
            }}

            .example-box {{
                padding: 2px 4px !important;
                border-left: 2px solid #2563eb !important;
                background: #f8fafc !important;
                margin: 0 !important;
                gap: 3px !important;
            }}

            .ex-icon {{
                display: none !important;
            }}

            .example-text {{
                font-size: 6.6pt !important;
                line-height: 1.18 !important;
                color: #475569 !important;
            }}

            .deriv-row {{
                padding: 2px 4px !important;
                background: #f8fafc !important;
                border-radius: 3px !important;
                gap: 1px !important;
            }}

            .deriv-title {{
                font-size: 5.4pt !important;
                font-weight: 700 !important;
                margin-bottom: 1px !important;
            }}

            .deriv-tags {{
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 2px 4px !important;
            }}

            .deriv-badge {{
                font-size: 6.1pt !important;
                border: 1px solid #e2e8f0 !important;
                padding: 0 3px !important;
                line-height: 1.15 !important;
                background: #ffffff !important;
                width: auto !important;
            }}

            .tr-footer {{
                padding-top: 2px !important;
                margin-top: 1px !important;
                border-top: 1px dashed #e2e8f0 !important;
            }}

            .tr-label {{
                font-size: 6.2pt !important;
                font-weight: 700 !important;
            }}

            .tr-interactive {{
                background: #fef2f2 !important;
                border: 1px solid #fecaca !important;
                padding: 1px 4px !important;
                border-radius: 3px !important;
            }}

            .tr-content {{
                font-size: 6.8pt !important;
                font-weight: 700 !important;
                color: #b91c1c !important;
            }}
        }}

        .print-header {{
            display: none;
        }}
    
        /* ========================================================
           DUOLINGO SORU MODU & APP NAVIGATION STYLES
           ======================================================== */
        :root {{
            --duo-green: #58cc02;
            --duo-green-dark: #46a302;
            --duo-green-shadow: #3b8702;
            --duo-green-bg: #eafbe7;
            --duo-green-border: #a5e998;
            --duo-green-text: #1b5e20;
            --duo-red: #ff4b4b;
            --duo-red-dark: #ea2b2b;
            --duo-red-shadow: #c91b1b;
            --duo-red-bg: #ffeded;
            --duo-red-border: #fca5a5;
            --duo-red-text: #991b1b;
            --duo-blue: #1cb0f6;
            --duo-blue-dark: #1899d6;
            --duo-yellow: #ffc800;
            --duo-yellow-dark: #e5a400;
            --duo-card-bg: #ffffff;
            --duo-card-border: #e2e8f0;
            --duo-card-border-bottom: #cbd5e1;
            --duo-card-hover: #f8fafc;
            --duo-card-active: #f1f5f9;
        }}

        [data-theme="dark"] {{
            --duo-green: #22c55e;
            --duo-green-dark: #16a34a;
            --duo-green-shadow: #15803d;
            --duo-green-bg: #052e16;
            --duo-green-border: #15803d;
            --duo-green-text: #86efac;
            --duo-red: #ef4444;
            --duo-red-dark: #dc2626;
            --duo-red-shadow: #b91c1c;
            --duo-red-bg: #450a0a;
            --duo-red-border: #991b1b;
            --duo-red-text: #fca5a5;
            --duo-blue: #38bdf8;
            --duo-blue-dark: #0284c7;
            --duo-yellow: #facc15;
            --duo-yellow-dark: #ca8a04;
            --duo-card-bg: #131b2e;
            --duo-card-border: #1e293b;
            --duo-card-border-bottom: #334155;
            --duo-card-hover: #1e293b;
            --duo-card-active: #0f172a;
        }}

        /* App Navigation Bar */
        .app-nav-bar {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            background: var(--bg-card);
            padding: 8px;
            border-radius: 16px;
            border: 1px solid var(--border-card);
            box-shadow: var(--shadow-sm);
        }}

        .nav-tab {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 14px 20px;
            border-radius: 12px;
            font-family: inherit;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-muted);
            background: transparent;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .nav-tab:hover {{
            background: var(--bg-body);
            color: var(--text-main);
        }}

        .nav-tab.active {{
            background: var(--primary);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }}

        .nav-tab.duo-nav-tab.active {{
            background: var(--duo-green);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(88, 204, 2, 0.35);
        }}

        .tab-icon {{
            font-size: 1.25rem;
        }}

        .tab-count, .tab-badge {{
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 999px;
            font-weight: 800;
        }}

        .tab-count {{
            background: rgba(0,0,0,0.06);
            color: inherit;
        }}

        .nav-tab.active .tab-count {{
            background: rgba(255,255,255,0.25);
            color: #ffffff;
        }}

        .tab-badge {{
            background: #ff4b4b;
            color: #ffffff;
            animation: pulse-badge 2s infinite;
        }}

        @keyframes pulse-badge {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.08); }}
        }}

        .btn-duo-cta {{
            background: linear-gradient(135deg, #58cc02, #22c55e) !important;
            color: #ffffff !important;
            border: 1px solid #46a302 !important;
            font-weight: 700 !important;
            box-shadow: 0 3px 0 #3b8702, 0 4px 10px rgba(88, 204, 2, 0.25) !important;
        }}

        .btn-duo-cta:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 0 #3b8702, 0 6px 14px rgba(88, 204, 2, 0.35) !important;
        }}

        .btn-duo-cta:active {{
            transform: translateY(2px);
            box-shadow: 0 1px 0 #3b8702 !important;
        }}

        /* Duolingo Quiz Screen Container */
        #quizView {{
            width: 100%;
        }}

        .quiz-screen {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 32px 28px;
            box-shadow: var(--shadow-md);
            margin-bottom: 24px;
            position: relative;
        }}

        /* Duolingo 3D Action Buttons */
        .duo-btn {{
            appearance: none;
            border: none;
            font-family: inherit;
            font-weight: 800;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.12s ease;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-decoration: none;
            user-select: none;
        }}

        .duo-btn-primary {{
            background: var(--duo-green);
            color: #ffffff;
            box-shadow: 0 4px 0 var(--duo-green-shadow);
        }}

        .duo-btn-primary:hover:not(:disabled) {{
            background: var(--duo-green-dark);
            transform: translateY(-1px);
            box-shadow: 0 5px 0 var(--duo-green-shadow);
        }}

        .duo-btn-primary:active:not(:disabled) {{
            transform: translateY(3px);
            box-shadow: 0 1px 0 var(--duo-green-shadow);
        }}

        .duo-btn-danger {{
            background: var(--duo-red);
            color: #ffffff;
            box-shadow: 0 4px 0 var(--duo-red-shadow);
        }}

        .duo-btn-danger:hover:not(:disabled) {{
            background: var(--duo-red-dark);
            transform: translateY(-1px);
            box-shadow: 0 5px 0 var(--duo-red-shadow);
        }}

        .duo-btn-danger:active:not(:disabled) {{
            transform: translateY(3px);
            box-shadow: 0 1px 0 var(--duo-red-shadow);
        }}

        .duo-btn-secondary {{
            background: var(--bg-body);
            color: var(--text-main);
            border: 2px solid var(--duo-card-border);
            box-shadow: 0 4px 0 var(--duo-card-border-bottom);
        }}

        .duo-btn-secondary:hover:not(:disabled) {{
            background: var(--duo-card-hover);
        }}

        .duo-btn-secondary:active:not(:disabled) {{
            transform: translateY(3px);
            box-shadow: 0 1px 0 var(--duo-card-border-bottom);
        }}

        .duo-btn-disabled, .duo-btn:disabled {{
            background: #e2e8f0 !important;
            color: #94a3b8 !important;
            box-shadow: 0 4px 0 #cbd5e1 !important;
            cursor: not-allowed !important;
            transform: none !important;
        }}

        [data-theme="dark"] .duo-btn-disabled, [data-theme="dark"] .duo-btn:disabled {{
            background: #1e293b !important;
            color: #64748b !important;
            box-shadow: 0 4px 0 #0f172a !important;
        }}

        .duo-btn-lg {{
            padding: 16px 28px;
            font-size: 1.05rem;
        }}

        .duo-btn-md {{
            padding: 12px 22px;
            font-size: 0.95rem;
        }}

        /* SETUP SCREEN */
        .duo-header-banner {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 28px;
            padding-bottom: 24px;
            border-bottom: 2px solid var(--border-card);
        }}

        .duo-mascot-avatar {{
            width: 76px;
            height: 76px;
            border-radius: 20px;
            background: linear-gradient(135deg, #d7ffb8, #86efac);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.8rem;
            box-shadow: 0 6px 16px rgba(88, 204, 2, 0.25);
            flex-shrink: 0;
            border: 2px solid #58cc02;
        }}

        [data-theme="dark"] .duo-mascot-avatar {{
            background: linear-gradient(135deg, #052e16, #14532d);
            border-color: #22c55e;
        }}

        .duo-banner-text h2 {{
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
            color: var(--text-main);
        }}

        .duo-banner-text p {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        .setup-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }}

        .setup-card {{
            background: var(--bg-body);
            border: 2px solid var(--border-card);
            border-radius: 16px;
            padding: 20px;
        }}

        .setup-card-title {{
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .setup-select {{
            width: 100%;
            padding: 12px 14px;
            border-radius: 12px;
            font-family: inherit;
            font-size: 0.95rem;
            font-weight: 600;
            border: 2px solid var(--border-card);
            background: var(--bg-card);
            color: var(--text-main);
            outline: none;
            cursor: pointer;
            transition: border-color 0.15s ease;
        }}

        .setup-select:focus {{
            border-color: var(--duo-green);
        }}

        .setup-actions {{
            display: flex;
            justify-content: center;
            gap: 16px;
            padding-top: 10px;
        }}

        .setup-stats-summary {{
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px dashed var(--border-card);
            color: var(--text-muted);
            font-size: 0.88rem;
            flex-wrap: wrap;
        }}

        .setup-stat-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .setup-stat-pill strong {{
            color: var(--text-main);
            font-weight: 800;
        }}

        /* PLAY SCREEN */
        .quiz-top-bar {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 28px;
        }}

        .quiz-close-btn {{
            appearance: none;
            border: none;
            background: transparent;
            font-size: 1.5rem;
            color: var(--text-muted);
            cursor: pointer;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s ease;
        }}

        .quiz-close-btn:hover {{
            background: var(--bg-body);
            color: var(--text-main);
        }}

        /* Duolingo Progress Bar */
        .duo-progress-container {{
            flex: 1;
            height: 18px;
            background: #e5e7eb;
            border-radius: 999px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
        }}

        [data-theme="dark"] .duo-progress-container {{
            background: #1e293b;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
        }}

        .duo-progress-fill {{
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #58cc02, #22c55e);
            border-radius: 999px;
            transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}

        .duo-progress-fill::after {{
            content: '';
            position: absolute;
            top: 2px;
            left: 4px;
            right: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.45);
            border-radius: 999px;
        }}

        .quiz-status-pill {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 800;
            font-size: 0.95rem;
            padding: 6px 14px;
            border-radius: 999px;
            background: var(--bg-body);
            border: 1px solid var(--border-card);
            color: var(--text-main);
        }}

        .streak-pill {{
            color: #ea580c;
        }}

        .duo-icon-btn {{
            appearance: none;
            border: 1px solid var(--border-card);
            background: var(--bg-body);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.15s ease;
        }}

        .duo-icon-btn:hover {{
            background: var(--bg-card);
            border-color: var(--duo-green);
        }}

        .duo-icon-btn.muted {{
            opacity: 0.5;
        }}

        /* Question Box */
        .question-box {{
            max-width: 820px;
            margin: 0 auto;
        }}

        .question-meta-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .question-type-badge {{
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 999px;
            background: #eff6ff;
            color: #2563eb;
            border: 1px solid #bfdbfe;
        }}

        [data-theme="dark"] .question-type-badge {{
            background: #1e3a8a;
            color: #93c5fd;
            border-color: #1e40af;
        }}

        .question-unit-tag {{
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .question-title {{
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 20px;
            line-height: 1.35;
        }}

        /* Prompt Display Card */
        .prompt-card {{
            background: var(--bg-body);
            border: 2px solid var(--border-card);
            border-radius: 18px;
            padding: 24px 28px;
            margin-bottom: 28px;
            position: relative;
        }}

        .prompt-sentence {{
            font-size: 1.25rem;
            line-height: 1.6;
            color: var(--text-main);
            font-weight: 500;
        }}

        .prompt-sentence .sentence-blank {{
            display: inline-block;
            background: var(--bg-card);
            border: 2px dashed #94a3b8;
            padding: 2px 14px;
            border-radius: 8px;
            font-weight: 800;
            color: var(--primary);
            margin: 0 4px;
            min-width: 120px;
            text-align: center;
        }}

        .prompt-word-head {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }}

        .prompt-word-text {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }}

        .prompt-word-pos {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--accent-pos);
            background: var(--accent-pos-bg);
            padding: 3px 10px;
            border-radius: 8px;
        }}

        .prompt-word-clue {{
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }}

        .prompt-audio-btn {{
            appearance: none;
            border: none;
            background: #eff6ff;
            color: #2563eb;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            cursor: pointer;
            box-shadow: 0 3px 0 #93c5fd;
            transition: all 0.12s ease;
            vertical-align: middle;
            margin-left: 8px;
        }}

        .prompt-audio-btn:hover {{
            background: #dbeafe;
            transform: translateY(-1px);
        }}

        .prompt-audio-btn:active {{
            transform: translateY(2px);
            box-shadow: 0 1px 0 #93c5fd;
        }}

        /* Options Grid */
        .options-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 28px;
        }}

        @media (max-width: 680px) {{
            .options-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .duo-option {{
            background: var(--duo-card-bg);
            border: 2px solid var(--duo-card-border);
            border-bottom: 5px solid var(--duo-card-border-bottom);
            border-radius: 16px;
            padding: 18px 20px;
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
            transition: all 0.12s ease;
            text-align: left;
            user-select: none;
        }}

        .duo-option:hover:not(.disabled) {{
            background: var(--duo-card-hover);
            border-color: #cbd5e1;
            transform: translateY(-2px);
        }}

        .duo-option:active:not(.disabled) {{
            transform: translateY(2px);
            border-bottom-width: 2px;
        }}

        .duo-option.selected {{
            border-color: #3b82f6;
            border-bottom-color: #1d4ed8;
            background: #eff6ff;
        }}

        [data-theme="dark"] .duo-option.selected {{
            background: #1e293b;
            border-color: #38bdf8;
            border-bottom-color: #0284c7;
        }}

        .duo-option.option-correct {{
            border-color: var(--duo-green) !important;
            border-bottom-color: var(--duo-green-dark) !important;
            background: var(--duo-green-bg) !important;
            animation: pop-bounce 0.3s ease;
        }}

        .duo-option.option-wrong {{
            border-color: var(--duo-red) !important;
            border-bottom-color: var(--duo-red-dark) !important;
            background: var(--duo-red-bg) !important;
            animation: shake 0.4s ease;
        }}

        @keyframes pop-bounce {{
            0% {{ transform: scale(0.96); }}
            60% {{ transform: scale(1.03); }}
            100% {{ transform: scale(1); }}
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20%, 60% {{ transform: translateX(-6px); }}
            40%, 80% {{ transform: translateX(6px); }}
        }}

        .option-key-badge {{
            width: 32px;
            height: 32px;
            border-radius: 10px;
            border: 1.5px solid var(--border-card);
            background: var(--bg-card);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.85rem;
            color: var(--text-muted);
            flex-shrink: 0;
        }}

        .duo-option.selected .option-key-badge {{
            border-color: #3b82f6;
            color: #2563eb;
            background: #ffffff;
        }}

        .duo-option.option-correct .option-key-badge {{
            border-color: var(--duo-green);
            color: #ffffff;
            background: var(--duo-green);
        }}

        .duo-option.option-wrong .option-key-badge {{
            border-color: var(--duo-red);
            color: #ffffff;
            background: var(--duo-red);
        }}

        .option-label-text {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-main);
            flex: 1;
        }}

        /* DUOLINGO BOTTOM DRAWER (FEEDBACK SHEET) */
        .duo-bottom-sheet {{
            margin-top: 24px;
            border-radius: 18px;
            padding: 24px 28px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            background: var(--bg-body);
            border: 2px solid var(--border-card);
        }}

        .duo-bottom-sheet.state-default {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            background: transparent;
            border: none;
            padding: 0;
        }}

        .duo-bottom-sheet.state-correct {{
            background: var(--duo-green-bg);
            border-color: var(--duo-green-border);
            color: var(--duo-green-text);
        }}

        .duo-bottom-sheet.state-wrong {{
            background: var(--duo-red-bg);
            border-color: var(--duo-red-border);
            color: var(--duo-red-text);
        }}

        .feedback-content-row {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .feedback-main-info {{
            display: flex;
            align-items: flex-start;
            gap: 16px;
            flex: 1;
            min-width: 280px;
        }}

        .feedback-status-icon {{
            width: 52px;
            height: 52px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            font-weight: 900;
            flex-shrink: 0;
            color: #ffffff;
        }}

        .state-correct .feedback-status-icon {{
            background: var(--duo-green);
            box-shadow: 0 4px 0 var(--duo-green-shadow);
        }}

        .state-wrong .feedback-status-icon {{
            background: var(--duo-red);
            box-shadow: 0 4px 0 var(--duo-red-shadow);
        }}

        .feedback-text-group h3 {{
            font-size: 1.4rem;
            font-weight: 900;
            margin-bottom: 6px;
        }}

        .state-correct .feedback-text-group h3 {{
            color: var(--duo-green-text);
        }}

        .state-wrong .feedback-text-group h3 {{
            color: var(--duo-red-text);
        }}

        .correct-answer-banner {{
            font-size: 1.15rem;
            font-weight: 800;
            margin-bottom: 8px;
            color: var(--duo-red-text);
        }}

        .correct-answer-banner strong {{
            text-decoration: underline;
            font-size: 1.3rem;
            color: var(--duo-red);
        }}

        .feedback-card-detail {{
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            padding: 12px 16px;
            margin-top: 8px;
            font-size: 0.92rem;
            line-height: 1.5;
            color: var(--text-main);
            border: 1px solid rgba(0,0,0,0.06);
        }}

        [data-theme="dark"] .feedback-card-detail {{
            background: rgba(0, 0, 0, 0.35);
            border-color: rgba(255,255,255,0.1);
        }}

        .detail-sentence {{
            font-style: italic;
            margin-top: 6px;
            color: var(--text-main);
        }}

        .highlight-word {{
            background: #fef08a;
            color: #854d0e;
            padding: 1px 6px;
            border-radius: 4px;
            font-weight: 700;
            font-style: normal;
        }}

        [data-theme="dark"] .highlight-word {{
            background: #854d0e;
            color: #fef08a;
        }}

        .feedback-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
            align-self: center;
        }}

        /* RESULTS SCREEN */
        .results-box {{
            max-width: 820px;
            margin: 0 auto;
            text-align: center;
        }}

        .results-trophy {{
            font-size: 4.5rem;
            margin-bottom: 16px;
            animation: bounce-trophy 1.2s infinite alternate ease-in-out;
        }}

        @keyframes bounce-trophy {{
            from {{ transform: translateY(0); }}
            to {{ transform: translateY(-10px) scale(1.05); }}
        }}

        .results-box h2 {{
            font-size: 2rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
            color: var(--text-main);
        }}

        .results-box p {{
            color: var(--text-muted);
            font-size: 1.05rem;
            margin-bottom: 28px;
        }}

        .results-stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 32px;
        }}

        @media (max-width: 640px) {{
            .results-stat-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .res-stat-card {{
            background: var(--bg-body);
            border: 2px solid var(--border-card);
            border-radius: 16px;
            padding: 16px;
            text-align: center;
        }}

        .res-stat-val {{
            font-size: 1.8rem;
            font-weight: 900;
            margin-bottom: 4px;
            color: var(--text-main);
        }}

        .res-stat-label {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .results-word-list-box {{
            background: var(--bg-body);
            border: 2px solid var(--border-card);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 28px;
            text-align: left;
            max-height: 380px;
            overflow-y: auto;
        }}

        .results-word-list-header {{
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 12px;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .results-word-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 14px;
            border-radius: 10px;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            margin-bottom: 8px;
            gap: 12px;
        }}

        .res-word-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .res-word-tag {{
            font-size: 0.75rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 6px;
        }}

        .tag-correct {{
            background: #dcfce7;
            color: #15803d;
        }}

        .tag-wrong {{
            background: #fee2e2;
            color: #b91c1c;
        }}

        [data-theme="dark"] .tag-correct {{
            background: #14532d;
            color: #86efac;
        }}

        [data-theme="dark"] .tag-wrong {{
            background: #7f1d1d;
            color: #fca5a5;
        }}

        .res-word-title {{
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-main);
        }}

        .res-word-tr {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .results-actions {{
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
        }}

        /* Print Override */
        @media print {{
            .app-nav-bar, #quizView, .btn-duo-cta {{
                display: none !important;
            }}
            #listView {{
                display: block !important;
            }}
        }}

    </style>
</head>
<body>
    <div class="container">
        <!-- Visible only when printing -->
        <div class="print-header">
            <h1>Kadir Has Üniversitesi - Hazırlık Track 3 Akademik Kelime Listesi</h1>
            <p>520 Kelime &bull; Longman Tanımları ve Örnek Cümleleri &bull; Ters Türkçe Anlamlarla Ezber Kağıdı</p>
        </div>

        <header>
            <div class="header-top">
                <div class="title-group">
                    <h1>Kadir Has Üniversitesi &bull; Track 3 Kelime Rehberi</h1>
                    <p>Hazırlık yılı için eksiksiz ve Longman kaynaklı 520 kelimelik akademik çalışma sistemi.</p>
                </div>
                <div class="header-actions">
                    <button class="btn btn-duo-cta" onclick="switchAppMode('quiz')">
                        🦉 Duolingo Soru Modu
                    </button>
                    <button class="btn" onclick="toggleAllTurkish()" id="toggleTrBtn">
                        🔄 Tüm Türkçe Çevirileri Aç / Kapat
                    </button>
                    <select class="btn" id="printColSelect" onchange="changePrintCols(this.value)" title="Yazdırma Sütun Sayısı" style="cursor:pointer; font-weight:600;">
                        <option value="3" selected>🖨️ 3 Sütun (Tasarruflu: ~20-24 Sayfa)</option>
                        <option value="2">🖨️ 2 Sütun (Standart: ~32-35 Sayfa)</option>
                    </select>
                    <button class="btn btn-primary" onclick="window.print()">
                        🖨️ Yazdır / PDF Kaydet
                    </button>
                    <button class="btn" onclick="toggleTheme()" id="themeBtn">
                        🌙 Koyu Mod
                    </button>
                </div>
            </div>

            <div class="stats-bar">
                <div class="stat-item">
                    <span>Toplam Kelime:</span>
                    <strong>{total_words}</strong>
                </div>
                <div class="stat-item">
                    <span>Toplam Ünite:</span>
                    <strong>10 Ünite</strong>
                </div>
                <div class="stat-item">
                    <span>Kaynak Standartı:</span>
                    <strong>Longman Dictionary of Contemporary English</strong>
                </div>
                <div class="stat-item">
                    <span>Ezber Formatı:</span>
                    <strong>Ters Türkçe (Self-Test Friendly)</strong>
                </div>
            </div>
        </header>

        <!-- App Mode Navigation Tabs -->
        <nav class="app-nav-bar" id="appNavBar">
            <button class="nav-tab active" id="tabList" onclick="switchAppMode('list')">
                <span class="tab-icon">📖</span>
                <span class="tab-label">Kelime Rehberi &amp; Kartlar</span>
                <span class="tab-count">{total_words}</span>
            </button>
            <button class="nav-tab duo-nav-tab" id="tabQuiz" onclick="switchAppMode('quiz')">
                <span class="tab-icon">🦉</span>
                <span class="tab-label">Duolingo Soru Modu</span>
                <span class="tab-badge">Canlı Pratik</span>
            </button>
        </nav>

        <!-- VIEW 1: WORD CARDS & LIST -->
        <div id="listView">
            <section class="controls-card">
            <div class="search-box">
                <input type="text" id="searchInput" class="search-input" placeholder="🔍 Kelime, Türkçe anlam veya tanım ara... (Örn: bond, analyse, kentsel)" oninput="filterCards()">
            </div>
            <div class="unit-filter" id="unitFilterGroup">
                <button class="unit-pill active" onclick="setUnitFilter('ALL', this)">Tümü (520)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 1', this)">Unit 1 (60)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 2', this)">Unit 2 (62)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 3', this)">Unit 3 (51)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 4', this)">Unit 4 (76)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 5', this)">Unit 5 (45)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 6', this)">Unit 6 (50)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 7', this)">Unit 7 (53)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 8', this)">Unit 8 (43)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 9', this)">Unit 9 (36)</button>
                <button class="unit-pill" onclick="setUnitFilter('Unit 10', this)">Unit 10 (44)</button>
            </div>
        </section>

        <main class="vocab-grid" id="vocabGrid">
{html_cards_str}
        </main>
        </div><!-- /#listView -->

        <!-- VIEW 2: DUOLINGO QUIZ VIEW -->
        <div id="quizView" style="display: none;">
            <!-- SCREEN 1: QUIZ SETUP -->
            <div id="quizSetupScreen" class="quiz-screen">
                <div class="duo-header-banner">
                    <div class="duo-mascot-avatar">🦉</div>
                    <div class="duo-banner-text">
                        <h2>KHAS Prep &bull; Duolingo Soru &amp; Öğrenme Modu</h2>
                        <p>Kelimeleri, Türkçe karşılıklarını, Longman tanımlarını ve örnek cümlelerini çözerek pekiştirin. Yanlış cevaplarda detaylı açıklama gösterilir.</p>
                    </div>
                </div>

                <div class="setup-grid">
                    <div class="setup-card">
                        <div class="setup-card-title">📚 1. Ünite Seçimi</div>
                        <select id="setupUnitSelect" class="setup-select">
                            <option value="ALL">Tüm Üniteler (520 Kelime)</option>
                            <option value="Unit 1">Unit 1: Social Relationships (60 kelime)</option>
                            <option value="Unit 2">Unit 2: Science &amp; DNA (62 kelime)</option>
                            <option value="Unit 3">Unit 3: City Solutions (51 kelime)</option>
                            <option value="Unit 4">Unit 4: Danger Zones &amp; Planet (76 kelime)</option>
                            <option value="Unit 5">Unit 5: Travel &amp; Business (45 kelime)</option>
                            <option value="Unit 6">Unit 6: Product Design (50 kelime)</option>
                            <option value="Unit 7">Unit 7: Global Challenges (53 kelime)</option>
                            <option value="Unit 8">Unit 8: Medical Innovations (43 kelime)</option>
                            <option value="Unit 9">Unit 9: Languages &amp; Culture (36 kelime)</option>
                            <option value="Unit 10">Unit 10: Survival &amp; Emotions (44 kelime)</option>
                        </select>
                    </div>

                    <div class="setup-card">
                        <div class="setup-card-title">🎯 2. Soru Türü</div>
                        <select id="setupTypeSelect" class="setup-select">
                            <option value="mixed">🔀 Karışık (Cümle, Anlam ve Tanım) [Önerilen]</option>
                            <option value="sentence">📝 Örnek Cümle Tamamlama (Boşluk Doldurma)</option>
                            <option value="word_to_tr">🇹🇷 Kelime ➔ Türkçe Anlam</option>
                            <option value="tr_to_word">🇬🇧 Türkçe Anlam ➔ İngilizce Kelime</option>
                            <option value="def_to_word">📖 Longman Tanımı ➔ İngilizce Kelime</option>
                        </select>
                    </div>

                    <div class="setup-card">
                        <div class="setup-card-title">⚡ 3. Soru Sayısı</div>
                        <select id="setupCountSelect" class="setup-select">
                            <option value="10">10 Soru (Hızlı Alıştırma ~2 dk)</option>
                            <option value="20" selected>20 Soru (Standart Ders ~4 dk)</option>
                            <option value="50">50 Soru (Kapsamlı Sınav)</option>
                            <option value="all">Sonsuz / Tüm Ünite</option>
                        </select>
                    </div>
                </div>

                <div class="setup-actions">
                    <button class="duo-btn duo-btn-primary duo-btn-lg" onclick="startQuizSession()">
                        🚀 Alıştırmaya Başla
                    </button>
                </div>

                <div class="setup-stats-summary">
                    <div class="setup-stat-pill">🔥 Seri: <strong id="setupStreakCount">0</strong></div>
                    <div class="setup-stat-pill">🎯 Toplam Çözülen: <strong id="setupTotalSolved">0</strong></div>
                    <div class="setup-stat-pill">📊 Genel Başarı: <strong id="setupAccuracyRate">%0</strong></div>
                    <div class="setup-stat-pill">💡 İpucu: <strong>Klavyede 1-4 ve Enter tuşlarını kullanabilirsiniz.</strong></div>
                </div>
            </div>

            <!-- SCREEN 2: ACTIVE GAMEPLAY -->
            <div id="quizPlayScreen" class="quiz-screen" style="display: none;">
                <div class="quiz-top-bar">
                    <button class="quiz-close-btn" onclick="confirmQuitQuiz()" title="Alıştırmadan Çık">✕</button>
                    <div class="duo-progress-container">
                        <div id="quizProgressFill" class="duo-progress-fill"></div>
                    </div>
                    <div class="quiz-status-pill streak-pill" title="Seri">
                        🔥 <span id="quizStreakVal">0</span>
                    </div>
                    <div class="quiz-status-pill" id="quizCounterVal" title="Soru İlerlemesi">
                        1 / 10
                    </div>
                    <button class="duo-icon-btn" onclick="toggleSound()" id="soundToggleBtn" title="Sesi Aç/Kapat">
                        🔊
                    </button>
                </div>

                <div class="question-box">
                    <div class="question-meta-row">
                        <span id="questionTypeBadge" class="question-type-badge">Örnek Cümle Tamamlama</span>
                        <span id="questionUnitTag" class="question-unit-tag">Unit 1 &bull; Reading 1</span>
                    </div>

                    <h2 id="questionInstruction" class="question-title">Cümledeki boşluğa hangi kelime gelmelidir?</h2>

                    <div class="prompt-card" id="questionPromptCard">
                        <!-- Dynamically filled -->
                    </div>

                    <div class="options-grid" id="quizOptionsGrid">
                        <!-- 4 Options dynamically filled -->
                    </div>

                    <div id="quizBottomSheet" class="duo-bottom-sheet state-default">
                        <button class="duo-btn duo-btn-primary duo-btn-lg" id="quizCheckBtn" onclick="checkCurrentAnswer()" disabled>
                            KONTROL ET
                        </button>
                    </div>
                </div>
            </div>

            <!-- SCREEN 3: RESULTS -->
            <div id="quizResultScreen" class="quiz-screen" style="display: none;">
                <div class="results-box">
                    <div class="results-trophy">🏆</div>
                    <h2 id="resultsHeading">Harika İş! Dersi Tamamladın!</h2>
                    <p id="resultsSubheading">Kadir Has Track 3 kelimeleri üzerinde pratik yaptın.</p>

                    <div class="results-stat-grid">
                        <div class="res-stat-card">
                            <div class="res-stat-val" style="color: var(--duo-green);" id="resCorrectCount">0</div>
                            <div class="res-stat-label">Doğru</div>
                        </div>
                        <div class="res-stat-card">
                            <div class="res-stat-val" style="color: var(--duo-red);" id="resWrongCount">0</div>
                            <div class="res-stat-label">Yanlış</div>
                        </div>
                        <div class="res-stat-card">
                            <div class="res-stat-val" style="color: var(--duo-blue);" id="resAccuracyPercent">%0</div>
                            <div class="res-stat-label">Başarı Oranı</div>
                        </div>
                        <div class="res-stat-card">
                            <div class="res-stat-val" style="color: #ea580c;" id="resBestStreak">0</div>
                            <div class="res-stat-label">En Yüksek Seri</div>
                        </div>
                    </div>

                    <div class="results-word-list-box">
                        <div class="results-word-list-header">
                            <span>Bu Oturumda Karşılaştığınız Kelimeler</span>
                            <span id="resWordsTotalBadge">10 Kelime</span>
                        </div>
                        <div id="resWordsContainer">
                            <!-- List of items -->
                        </div>
                    </div>

                    <div class="results-actions">
                        <button class="duo-btn duo-btn-danger duo-btn-md" id="repeatMistakesBtn" onclick="repeatMistakesOnly()" style="display: none;">
                            🔁 Hatalı Kelimeleri Tekrarla (<span id="mistakeBtnCount">0</span>)
                        </button>
                        <button class="duo-btn duo-btn-primary duo-btn-md" onclick="showQuizSetup()">
                            🚀 Yeni Alıştırma Yap
                        </button>
                        <button class="duo-btn duo-btn-secondary duo-btn-md" onclick="switchAppMode('list')">
                            📚 Kelime Listesine Dön
                        </button>
                    </div>
                </div>
            </div>
        </div><!-- /#quizView -->
    </div>

    <script>
        // ==========================================
        // KHAS VOCABULARY DATABASE & DUOLINGO ENGINE
        // ==========================================
        const ALL_VOCAB = {vocab_json_str};

        let currentUnit = 'ALL';
        let allReversed = true;

        function setUnitFilter(unit, element) {{
            currentUnit = unit;
            document.querySelectorAll('.unit-pill').forEach(pill => pill.classList.remove('active'));
            element.classList.add('active');
            filterCards();
        }}

        function filterCards() {{
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            const cards = document.querySelectorAll('.vocab-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const cardUnit = card.getAttribute('data-unit');
                const cardWord = card.getAttribute('data-word');
                const cardTr = card.getAttribute('data-tr');
                const textContent = card.innerText.toLowerCase();

                const matchesUnit = (currentUnit === 'ALL' || cardUnit === currentUnit);
                const matchesSearch = !query || cardWord.includes(query) || cardTr.includes(query) || textContent.includes(query);

                if (matchesUnit && matchesSearch) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function toggleCardTr(container) {{
            const textEl = container.querySelector('.tr-content');
            const hintEl = container.querySelector('.flip-hint');
            const card = container.closest('.vocab-card');
            const normal = card.getAttribute('data-tr');
            
            if (textEl.classList.contains('reversed')) {{
                textEl.innerText = normal;
                textEl.classList.remove('reversed');
                textEl.style.color = 'var(--primary)';
                hintEl.innerText = '⟲ gizle';
            }} else {{
                textEl.innerText = reverseString(normal);
                textEl.classList.add('reversed');
                textEl.style.color = 'var(--tr-text)';
                hintEl.innerText = '⟲ çevir';
            }}
        }}

        function reverseString(str) {{
            return str.split('').reverse().join('');
        }}

        function toggleAllTurkish() {{
            allReversed = !allReversed;
            const btn = document.getElementById('toggleTrBtn');
            btn.innerText = allReversed ? '🔄 Tüm Türkçe Çevirileri Aç' : '🔄 Tüm Türkçe Çevirileri Ters Yap';

            document.querySelectorAll('.vocab-card').forEach(card => {{
                const container = card.querySelector('.tr-interactive');
                const textEl = container.querySelector('.tr-content');
                const hintEl = container.querySelector('.flip-hint');
                const normal = card.getAttribute('data-tr');

                if (allReversed) {{
                    textEl.innerText = reverseString(normal);
                    textEl.classList.add('reversed');
                    textEl.style.color = 'var(--tr-text)';
                    hintEl.innerText = '⟲ çevir';
                }} else {{
                    textEl.innerText = normal;
                    textEl.classList.remove('reversed');
                    textEl.style.color = 'var(--primary)';
                    hintEl.innerText = '⟲ gizle';
                }}
            }});
        }}

        function changePrintCols(val) {{
            if (val === '2') {{
                document.body.classList.add('print-2col');
            }} else {{
                document.body.classList.remove('print-2col');
            }}
        }}

        function toggleTheme() {{
            const body = document.documentElement;
            const btn = document.getElementById('themeBtn');
            const isDark = body.getAttribute('data-theme') === 'dark';
            if (isDark) {{
                body.removeAttribute('data-theme');
                btn.innerText = '🌙 Koyu Mod';
            }} else {{
                body.setAttribute('data-theme', 'dark');
                btn.innerText = '☀️ Açık Mod';
            }}
        }}

        // ==========================================
        // DUOLINGO PRACTICE ENGINE
        // ==========================================
        let soundEnabled = true;

        let quizState = {{
            active: false,
            currentMode: 'list',
            questionQueue: [],
            currentIndex: 0,
            totalCount: 0,
            score: 0,
            wrong: 0,
            streak: 0,
            maxStreak: 0,
            answered: false,
            selectedOption: null,
            activeQuestion: null,
            history: [],
            mistakes: []
        }};

        // App Mode Switcher (List vs Duolingo Quiz)
        function switchAppMode(mode) {{
            quizState.currentMode = mode;
            const tabList = document.getElementById('tabList');
            const tabQuiz = document.getElementById('tabQuiz');
            const listView = document.getElementById('listView');
            const quizView = document.getElementById('quizView');

            if (mode === 'list') {{
                tabList.classList.add('active');
                tabQuiz.classList.remove('active');
                listView.style.display = 'block';
                quizView.style.display = 'none';
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }} else {{
                tabList.classList.remove('active');
                tabQuiz.classList.add('active');
                listView.style.display = 'none';
                quizView.style.display = 'block';
                updateSetupStatsUI();
                if (!quizState.active) {{
                    showQuizSetup();
                }}
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}

        // Sound Synthesis (Web Audio API - Offline & Zero-Latency)
        function playQuizSound(type) {{
            if (!soundEnabled) return;
            try {{
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (!AudioCtx) return;
                const ctx = new AudioCtx();
                const now = ctx.currentTime;

                if (type === 'correct') {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(523.25, now);       // C5
                    osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
                    osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
                    osc.frequency.setValueAtTime(1046.50, now + 0.24);// C6
                    gain.gain.setValueAtTime(0.12, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 0.5);
                }} else if (type === 'wrong') {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(260, now);
                    osc.frequency.setValueAtTime(200, now + 0.14);
                    gain.gain.setValueAtTime(0.14, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 0.45);
                }} else if (type === 'click') {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(620, now);
                    gain.gain.setValueAtTime(0.05, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 0.06);
                }} else if (type === 'fanfare') {{
                    [523.25, 659.25, 783.99, 1046.50].forEach((freq, idx) => {{
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freq, now + (idx * 0.12));
                        gain.gain.setValueAtTime(0.12, now + (idx * 0.12));
                        gain.gain.exponentialRampToValueAtTime(0.001, now + (idx * 0.12) + 0.4);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(now + (idx * 0.12));
                        osc.stop(now + (idx * 0.12) + 0.4);
                    }});
                }}
            }} catch(e) {{}}
        }}

        function toggleSound() {{
            soundEnabled = !soundEnabled;
            const btn = document.getElementById('soundToggleBtn');
            if (btn) {{
                btn.innerHTML = soundEnabled ? '🔊' : '🔇';
                btn.classList.toggle('muted', !soundEnabled);
                btn.title = soundEnabled ? 'Sesi Kapat' : 'Sesi Aç';
            }}
        }}

        // Native English Pronunciation (Web Speech API)
        function speakText(text) {{
            if (!('speechSynthesis' in window)) return;
            try {{
                window.speechSynthesis.cancel();
                const clean = text.replace(/_+/g, 'blank').trim();
                const utter = new SpeechSynthesisUtterance(clean);
                utter.lang = 'en-US';
                utter.rate = 0.9;
                window.speechSynthesis.speak(utter);
            }} catch(e) {{}}
        }}

        // Audio Pronunciation Helpers
        function speakVocabWord(id) {{
            const item = ALL_VOCAB.find(w => w.id === id);
            if (item) speakText(item.word);
        }}

        function speakVocabExample(id) {{
            const item = ALL_VOCAB.find(w => w.id === id);
            if (item) speakText(item.example);
        }}

        function replayCurrentAudio() {{
            if (!quizState.activeQuestion) return;
            const q = quizState.activeQuestion;
            if (q.type === 'sentence') {{
                speakVocabExample(q.target.id);
            }} else {{
                speakVocabWord(q.target.id);
            }}
        }}

        // Helper: Format Sentence with Blank (No Regex Escaping Issues)
        function createBlankedSentence(sentence, word) {{
            if (!sentence || !word) return {{ display: sentence || '', raw: sentence || '' }};
            const tokens = sentence.split(/(\\s+|[.,!?;:'"()]+)/);
            const targetLower = word.toLowerCase().trim();
            let replaced = false;
            const result = tokens.map(token => {{
                const clean = token.toLowerCase().replace(/[^a-z]/g, '');
                if (!replaced && clean.length >= 3 && targetLower.length >= 3) {{
                    if (clean === targetLower || (clean.startsWith(targetLower) && clean.length <= targetLower.length + 4) || (targetLower.startsWith(clean) && targetLower.length <= clean.length + 3)) {{
                        replaced = true;
                        return '<span class="sentence-blank">__________</span>';
                    }}
                }}
                return token;
            }}).join('');

            if (replaced) {{
                return {{ display: result, raw: sentence }};
            }}
            return {{ display: sentence + ' <span class="sentence-blank">__________</span>', raw: sentence }};
        }}

        // Helper: Highlight word in sentence
        function createHighlightedSentence(sentence, word) {{
            if (!sentence || !word) return sentence || '';
            const tokens = sentence.split(/(\\s+|[.,!?;:'"()]+)/);
            const targetLower = word.toLowerCase().trim();
            let replaced = false;
            return tokens.map(token => {{
                const clean = token.toLowerCase().replace(/[^a-z]/g, '');
                if (!replaced && clean.length >= 3 && targetLower.length >= 3) {{
                    if (clean === targetLower || (clean.startsWith(targetLower) && clean.length <= targetLower.length + 4) || (targetLower.startsWith(clean) && targetLower.length <= clean.length + 3)) {{
                        replaced = true;
                        return '<span class="highlight-word">' + token + '</span>';
                    }}
                }}
                return token;
            }}).join('');
        }}

        // Helper: Shuffle Array (Fisher-Yates)
        function shuffleArray(arr) {{
            const copy = [...arr];
            for (let i = copy.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [copy[i], copy[j]] = [copy[j], copy[i]];
            }}
            return copy;
        }}

        // Screen Visibility Controls
        function showQuizSetup() {{
            quizState.active = false;
            document.getElementById('quizSetupScreen').style.display = 'block';
            document.getElementById('quizPlayScreen').style.display = 'none';
            document.getElementById('quizResultScreen').style.display = 'none';
            updateSetupStatsUI();
        }}

        function confirmQuitQuiz() {{
            if (quizState.active && !confirm('Alıştırmayı sonlandırmak ve ana menüye dönmek istiyor musunuz?')) {{
                return;
            }}
            showQuizSetup();
        }}

        function updateSetupStatsUI() {{
            try {{
                const streak = localStorage.getItem('khas_duo_streak') || '0';
                const total = localStorage.getItem('khas_duo_total') || '0';
                const correct = localStorage.getItem('khas_duo_correct') || '0';
                const acc = total > 0 ? Math.round((parseInt(correct) / parseInt(total)) * 100) : 0;

                const streakEl = document.getElementById('setupStreakCount');
                const totalEl = document.getElementById('setupTotalSolved');
                const accEl = document.getElementById('setupAccuracyRate');
                if (streakEl) streakEl.innerText = streak;
                if (totalEl) totalEl.innerText = total;
                if (accEl) accEl.innerText = '%' + acc;
            }} catch(e) {{}}
        }}

        // START QUIZ SESSION
        function startQuizSession(overrideWords = null) {{
            const unitVal = document.getElementById('setupUnitSelect').value;
            const countVal = document.getElementById('setupCountSelect').value;

            let pool = [];
            if (overrideWords && overrideWords.length > 0) {{
                pool = [...overrideWords];
            }} else {{
                if (unitVal === 'ALL') {{
                    pool = [...ALL_VOCAB];
                }} else {{
                    pool = ALL_VOCAB.filter(w => w.unit === unitVal);
                }}
            }}

            if (pool.length === 0) {{
                alert('Seçilen ünite için kelime bulunamadı.');
                return;
            }}

            pool = shuffleArray(pool);

            let questionCount = pool.length;
            if (countVal !== 'all') {{
                const requested = parseInt(countVal, 10);
                if (requested < pool.length) {{
                    questionCount = requested;
                    pool = pool.slice(0, requested);
                }}
            }}

            quizState.active = true;
            quizState.questionQueue = pool;
            quizState.currentIndex = 0;
            quizState.totalCount = pool.length;
            quizState.score = 0;
            quizState.wrong = 0;
            quizState.streak = 0;
            quizState.maxStreak = 0;
            quizState.answered = false;
            quizState.selectedOption = null;
            quizState.history = [];
            quizState.mistakes = [];

            document.getElementById('quizSetupScreen').style.display = 'none';
            document.getElementById('quizResultScreen').style.display = 'none';
            document.getElementById('quizPlayScreen').style.display = 'block';

            loadNextQuestion();
        }}

        function repeatMistakesOnly() {{
            if (!quizState.mistakes || quizState.mistakes.length === 0) return;
            startQuizSession(quizState.mistakes);
        }}

        // LOAD CURRENT QUESTION
        function loadNextQuestion() {{
            if (quizState.currentIndex >= quizState.totalCount) {{
                showQuizResults();
                return;
            }}

            quizState.answered = false;
            quizState.selectedOption = null;

            const curIdx = quizState.currentIndex;
            const total = quizState.totalCount;
            const targetWord = quizState.questionQueue[curIdx];

            // Progress bar & counters
            const pct = (curIdx / total) * 100;
            document.getElementById('quizProgressFill').style.width = pct + '%';
            document.getElementById('quizStreakVal').innerText = quizState.streak;
            document.getElementById('quizCounterVal').innerText = (curIdx + 1) + ' / ' + total;

            // Determine question type
            const chosenType = document.getElementById('setupTypeSelect').value;
            let type = chosenType;
            if (chosenType === 'mixed') {{
                const availableTypes = ['sentence', 'word_to_tr', 'tr_to_word', 'def_to_word'];
                type = availableTypes[Math.floor(Math.random() * availableTypes.length)];
            }}

            // Select 3 distractors
            let candidatePool = ALL_VOCAB.filter(w => w.word.toLowerCase() !== targetWord.word.toLowerCase());
            // Prefer words from same unit if possible
            const sameUnitPool = candidatePool.filter(w => w.unit === targetWord.unit);
            let distractors = [];
            if (sameUnitPool.length >= 3) {{
                distractors = shuffleArray(sameUnitPool).slice(0, 3);
            }} else {{
                distractors = shuffleArray(candidatePool).slice(0, 3);
            }}

            // Build Options based on Question Type
            let promptHtml = '';
            let instructionText = '';
            let badgeText = '';
            let options = [];
            let correctOptionText = '';

            if (type === 'sentence') {{
                badgeText = '📝 ÖRNEK CÜMLE TAMAMLAMA';
                instructionText = 'Cümledeki boşluğa hangi kelime gelmelidir?';
                const blankData = createBlankedSentence(targetWord.example, targetWord.word);
                promptHtml = `
                    <div class="prompt-sentence">
                        "${{blankData.display}}"
                        <button class="prompt-audio-btn" onclick="speakVocabExample(${{targetWord.id}})" title="Cümleyi Dinle">🔊</button>
                    </div>
                    <div class="prompt-word-clue" style="margin-top:12px;">
                        <span class="prompt-word-pos">${{targetWord.pos}}</span> &bull; <strong>İpucu (Türkçe):</strong> ${{targetWord.tr}}
                    </div>
                `;
                correctOptionText = targetWord.word;
                options = [
                    {{ text: targetWord.word, isCorrect: true }},
                    {{ text: distractors[0].word, isCorrect: false }},
                    {{ text: distractors[1].word, isCorrect: false }},
                    {{ text: distractors[2].word, isCorrect: false }}
                ];
            }} else if (type === 'word_to_tr') {{
                badgeText = '🇹🇷 KELİME ANLAMI';
                instructionText = 'Aşağıdaki kelimenin Türkçe anlamı hangisidir?';
                promptHtml = `
                    <div class="prompt-word-head">
                        <span class="prompt-word-text">${{targetWord.word}}</span>
                        <span class="prompt-word-pos">${{targetWord.pos}}</span>
                        <button class="prompt-audio-btn" onclick="speakVocabWord(${{targetWord.id}})" title="Telaffuzu Dinle">🔊</button>
                    </div>
                    <div class="prompt-word-clue">
                        <strong>Tanım:</strong> ${{targetWord.definition}}
                    </div>
                `;
                correctOptionText = targetWord.tr;
                options = [
                    {{ text: targetWord.tr, isCorrect: true }},
                    {{ text: distractors[0].tr, isCorrect: false }},
                    {{ text: distractors[1].tr, isCorrect: false }},
                    {{ text: distractors[2].tr, isCorrect: false }}
                ];
            }} else if (type === 'tr_to_word') {{
                badgeText = '🇬🇧 İNGİLİZCE KARŞILIĞI BUL';
                instructionText = 'Bu anlama gelen İngilizce kelime hangisidir?';
                promptHtml = `
                    <div class="prompt-word-head">
                        <span class="prompt-word-text" style="color:var(--primary); font-size:1.7rem;">${{targetWord.tr}}</span>
                        <span class="prompt-word-pos">${{targetWord.pos}}</span>
                    </div>
                    <div class="prompt-word-clue">
                        <strong>Longman Tanımı:</strong> "${{targetWord.definition}}"
                    </div>
                `;
                correctOptionText = targetWord.word;
                options = [
                    {{ text: targetWord.word, isCorrect: true }},
                    {{ text: distractors[0].word, isCorrect: false }},
                    {{ text: distractors[1].word, isCorrect: false }},
                    {{ text: distractors[2].word, isCorrect: false }}
                ];
            }} else {{
                // def_to_word
                badgeText = '📖 LONGMAN TANIMI';
                instructionText = 'Bu tanıma uyan İngilizce kelime hangisidir?';
                promptHtml = `
                    <div class="prompt-sentence">
                        "${{targetWord.definition}}"
                    </div>
                    <div class="prompt-word-clue" style="margin-top:12px;">
                        <span class="prompt-word-pos">${{targetWord.pos}}</span> &bull; <strong>Türkçe Anlamı:</strong> ${{targetWord.tr}}
                    </div>
                `;
                correctOptionText = targetWord.word;
                options = [
                    {{ text: targetWord.word, isCorrect: true }},
                    {{ text: distractors[0].word, isCorrect: false }},
                    {{ text: distractors[1].word, isCorrect: false }},
                    {{ text: distractors[2].word, isCorrect: false }}
                ];
            }}

            // Shuffle options
            const shuffledOptions = shuffleArray(options);
            const correctIndex = shuffledOptions.findIndex(o => o.isCorrect);

            quizState.activeQuestion = {{
                type: type,
                target: targetWord,
                options: shuffledOptions,
                correctIndex: correctIndex,
                correctText: correctOptionText
            }};

            // Render Meta, Title & Prompt
            document.getElementById('questionTypeBadge').innerText = badgeText;
            document.getElementById('questionUnitTag').innerText = targetWord.unit + ' • ' + (targetWord.section || 'Vocab');
            document.getElementById('questionInstruction').innerText = instructionText;
            document.getElementById('questionPromptCard').innerHTML = promptHtml;

            // Render Options
            const optGrid = document.getElementById('quizOptionsGrid');
            optGrid.innerHTML = '';
            shuffledOptions.forEach((opt, idx) => {{
                const btn = document.createElement('div');
                btn.className = 'duo-option';
                btn.id = 'duoOpt_' + idx;
                btn.onclick = () => selectOption(idx);
                btn.ondblclick = () => {{
                    selectOption(idx);
                    checkCurrentAnswer();
                }};
                btn.innerHTML = `
                    <div class="option-key-badge">${{idx + 1}}</div>
                    <div class="option-label-text">${{opt.text}}</div>
                `;
                optGrid.appendChild(btn);
            }});

            // Reset Bottom Sheet to Default
            const bottomSheet = document.getElementById('quizBottomSheet');
            bottomSheet.className = 'duo-bottom-sheet state-default';
            bottomSheet.innerHTML = `
                <button class="duo-btn duo-btn-primary duo-btn-lg" id="quizCheckBtn" onclick="checkCurrentAnswer()" disabled>
                    KONTROL ET
                </button>
            `;

            // Auto-speak in word questions if sound enabled
            if (type === 'word_to_tr') {{
                setTimeout(() => speakText(targetWord.word), 150);
            }}
        }}

        // SELECT OPTION
        function selectOption(index) {{
            if (quizState.answered) return;
            playQuizSound('click');
            quizState.selectedOption = index;

            document.querySelectorAll('.duo-option').forEach((el, idx) => {{
                el.classList.toggle('selected', idx === index);
            }});

            const checkBtn = document.getElementById('quizCheckBtn');
            if (checkBtn) {{
                checkBtn.disabled = false;
                checkBtn.classList.remove('duo-btn-disabled');
            }}
        }}

        // CHECK ANSWER
        function checkCurrentAnswer() {{
            if (quizState.answered || quizState.selectedOption === null) return;
            quizState.answered = true;

            const q = quizState.activeQuestion;
            const isCorrect = (quizState.selectedOption === q.correctIndex);
            const selectedEl = document.getElementById('duoOpt_' + quizState.selectedOption);
            const correctEl = document.getElementById('duoOpt_' + q.correctIndex);
            const bottomSheet = document.getElementById('quizBottomSheet');

            document.querySelectorAll('.duo-option').forEach(el => el.classList.add('disabled'));

            if (isCorrect) {{
                // CORRECT!
                playQuizSound('correct');
                if (selectedEl) selectedEl.classList.add('option-correct');

                quizState.score++;
                quizState.streak++;
                quizState.maxStreak = Math.max(quizState.maxStreak, quizState.streak);
                quizState.history.push({{ word: q.target, correct: true }});

                bottomSheet.className = 'duo-bottom-sheet state-correct';
                bottomSheet.innerHTML = `
                    <div class="feedback-content-row">
                        <div class="feedback-main-info">
                            <div class="feedback-status-icon">✓</div>
                            <div class="feedback-text-group">
                                <h3>Harika! Doğru Cevap</h3>
                                <div class="feedback-card-detail">
                                    <strong>${{q.target.word}}</strong> <span style="color:var(--accent-pos)">${{q.target.pos}}</span> &bull; <span>${{q.target.tr}}</span>
                                    <div class="detail-sentence">"${{createHighlightedSentence(q.target.example, q.target.word)}}"</div>
                                </div>
                            </div>
                        </div>
                        <div class="feedback-actions">
                            <button class="duo-icon-btn" onclick="speakVocabWord(${{q.target.id}})" title="Telaffuzu Dinle">🔊</button>
                            <button class="duo-btn duo-btn-primary duo-btn-lg" onclick="proceedToNext()">SONRAKİ ➔</button>
                        </div>
                    </div>
                `;
            }} else {{
                // WRONG! Show correct answer + learning card
                playQuizSound('wrong');
                if (selectedEl) selectedEl.classList.add('option-wrong');
                if (correctEl) correctEl.classList.add('option-correct');

                quizState.wrong++;
                quizState.streak = 0;
                quizState.mistakes.push(q.target);
                quizState.history.push({{ word: q.target, correct: false }});

                bottomSheet.className = 'duo-bottom-sheet state-wrong';
                bottomSheet.innerHTML = `
                    <div class="feedback-content-row">
                        <div class="feedback-main-info">
                            <div class="feedback-status-icon">✕</div>
                            <div class="feedback-text-group">
                                <h3>Yanlış!</h3>
                                <div class="correct-answer-banner">Doğru Yanıt: <strong>${{q.correctText}}</strong></div>
                                <div class="feedback-card-detail">
                                    <div><strong>${{q.target.word}}</strong> <span style="color:var(--accent-pos)">${{q.target.pos}}</span> &bull; <span>${{q.target.tr}}</span></div>
                                    <div style="margin-top:4px; font-size:0.88rem; color:var(--text-muted)"><strong>Longman Tanımı:</strong> ${{q.target.definition}}</div>
                                    <div class="detail-sentence"><strong>Örnek Cümle:</strong> "${{createHighlightedSentence(q.target.example, q.target.word)}}"</div>
                                    <div style="margin-top:6px; font-size:0.8rem; opacity:0.85;">💡 Bu kelime alıştırma sonundaki tekrar listenize eklendi.</div>
                                </div>
                            </div>
                        </div>
                        <div class="feedback-actions">
                            <button class="duo-icon-btn" onclick="speakVocabWord(${{q.target.id}})" title="Telaffuzu Dinle">🔊</button>
                            <button class="duo-btn duo-btn-danger duo-btn-lg" onclick="proceedToNext()">ANLADIM, DEVAM ET ➔</button>
                        </div>
                    </div>
                `;
            }}
        }}

        // PROCEED TO NEXT QUESTION
        function proceedToNext() {{
            quizState.currentIndex++;
            loadNextQuestion();
        }}

        // SHOW QUIZ RESULTS
        function showQuizResults() {{
            quizState.active = false;
            playQuizSound('fanfare');

            document.getElementById('quizPlayScreen').style.display = 'none';
            document.getElementById('quizResultScreen').style.display = 'block';

            const total = quizState.totalCount;
            const correct = quizState.score;
            const wrong = quizState.wrong;
            const acc = total > 0 ? Math.round((correct / total) * 100) : 0;

            document.getElementById('resCorrectCount').innerText = correct;
            document.getElementById('resWrongCount').innerText = wrong;
            document.getElementById('resAccuracyPercent').innerText = '%' + acc;
            document.getElementById('resBestStreak').innerText = '🔥 ' + quizState.maxStreak;
            document.getElementById('resWordsTotalBadge').innerText = total + ' Kelime';

            if (acc >= 80) {{
                document.getElementById('resultsHeading').innerText = '🎉 Muazzam Başarı! Harika İş Çıkardın!';
                document.getElementById('resultsSubheading').innerText = 'Kadir Has Track 3 kelimelerinde yüksek başarı sağladın.';
            }} else if (acc >= 50) {{
                document.getElementById('resultsHeading').innerText = '👏 Tebrikler! İyi Bir İlerleme Kaydettin!';
                document.getElementById('resultsSubheading').innerText = 'Hatalı kelimeleri tekrar ederek eksiklerini hızla kapatabilirsin.';
            }} else {{
                document.getElementById('resultsHeading').innerText = '💪 Alıştırma Tamamlandı!';
                document.getElementById('resultsSubheading').innerText = 'Öğrenme süreci tekrarla güçlenir. Hatalı kelimeleri tekrar çözerek pekiştir.';
            }}

            // Mistakes button
            const repeatBtn = document.getElementById('repeatMistakesBtn');
            const mistakeCountSpan = document.getElementById('mistakeBtnCount');
            if (quizState.mistakes.length > 0) {{
                repeatBtn.style.display = 'inline-flex';
                mistakeCountSpan.innerText = quizState.mistakes.length;
            }} else {{
                repeatBtn.style.display = 'none';
            }}

            // Render word list breakdown
            const resContainer = document.getElementById('resWordsContainer');
            resContainer.innerHTML = '';
            quizState.history.forEach(item => {{
                const row = document.createElement('div');
                row.className = 'results-word-item';
                row.innerHTML = `
                    <div class="res-word-left">
                        <span class="res-word-tag ${{item.correct ? 'tag-correct' : 'tag-wrong'}}">
                            ${{item.correct ? '✓ Doğru' : '✕ Hatalı'}}
                        </span>
                        <div>
                            <span class="res-word-title">${{item.word.word}}</span>
                            <span style="font-size:0.8rem; color:var(--accent-pos)">${{item.word.pos}}</span>
                            <div class="res-word-tr">${{item.word.tr}} &bull; <em style="font-size:0.8rem">"${{item.word.example}}"</em></div>
                        </div>
                    </div>
                    <button class="duo-icon-btn" onclick="speakVocabWord(${{item.word.id}})" title="Telaffuzu Dinle">🔊</button>
                `;
                resContainer.appendChild(row);
            }});

            // Save persistent stats
            try {{
                const prevStreak = parseInt(localStorage.getItem('khas_duo_streak') || '0', 10);
                const prevTotal = parseInt(localStorage.getItem('khas_duo_total') || '0', 10);
                const prevCorrect = parseInt(localStorage.getItem('khas_duo_correct') || '0', 10);

                localStorage.setItem('khas_duo_streak', Math.max(prevStreak, quizState.maxStreak));
                localStorage.setItem('khas_duo_total', prevTotal + total);
                localStorage.setItem('khas_duo_correct', prevCorrect + correct);
            }} catch(e) {{}}
        }}

        // Keyboard Controls (1-4, Enter, Space)
        document.addEventListener('keydown', function(e) {{
            const playScreen = document.getElementById('quizPlayScreen');
            if (playScreen && playScreen.style.display !== 'none') {{
                if (['1', '2', '3', '4'].includes(e.key)) {{
                    const idx = parseInt(e.key, 10) - 1;
                    selectOption(idx);
                }} else if (e.key === 'Enter') {{
                    if (!quizState.answered) {{
                        if (quizState.selectedOption !== null) {{
                            checkCurrentAnswer();
                        }}
                    }} else {{
                        proceedToNext();
                    }}
                }} else if (e.key === ' ' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'SELECT') {{
                    e.preventDefault();
                    replayCurrentAudio();
                }}
            }}
        }});
    </script>
</body>
</html>
'''

os.makedirs(os.path.join(base_dir, "dist"), exist_ok=True)
with open(os.path.join(base_dir, "dist", "standalone.html"), "w", encoding="utf-8") as f:
    f.write(html_template)

with open(os.path.join(base_dir, "data", "vocabulary.json"), "w", encoding="utf-8") as f:
    json.dump(vocab_json_list, f, ensure_ascii=False, indent=2)

with open(os.path.join(base_dir, "js", "default-data.js"), "w", encoding="utf-8") as f:
    f.write("// Built-in Academic English Vocabulary Dataset (520 Words Across 10 Units)\nconst DEFAULT_VOCABULARY = ")
    json.dump(vocab_json_list, f, ensure_ascii=False)
    f.write(";\n")

print("Build completed successfully (dist/standalone.html, data/vocabulary.json, js/default-data.js)!")
