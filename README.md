# さくら日本語 — Sakura Japanese Institute Textbooks

さくら日本語学院 (Sakura Japanese Institute), Char Baktaboli, Fatullah, Narayanganj, Bangladesh.
著者・監修: アハメド・サエム (Ahmed Sayem)

**Private — do not share publicly.**

| Folder | Book | Contents |
|---|---|---|
| `n5/` | さくら日本語 N5 | 22 lessons + kana + appendix · 104 kanji · ~700 words · reading in every lesson · `sakura-n5.pdf` (print) · `sakura-n5.html` (web) |
| `mock/` | JLPT mock test site | N5/N4 full mocks + 6 monthly tests that follow the two books · `jlpt-moshi.html` |
| `n4/` | さくら日本語 N4 | 24 lessons + appendix · 144 kanji · 120 grammar points · 673 words · reading in every lesson · `sakura-n4.pdf` (print) · `sakura-n4.html` (web) |

## Files in each folder
- `data1.js` … `data4.js` (N5 also `data5.js`: reading passages + extra vocabulary) — all book content (dialogues, vocabulary, grammar, kanji, reading, exercises). Furigana: `{漢字|かな}`. The correct choice is always written first; choices are shuffled automatically.
- `reader.html` — the book template (design + layout). `/*DATA*/` is replaced with the data files.
- `sakura-nX.html` — the finished web book (template + data).
- `build_pdf.py` — builds the print PDF (two-pass, Playwright Chromium, local fonts: Shippori Mincho, Hind Siliguri, etc.). Usage: `python3 build_pdf.py <fonts-dir>`.

## Editing
To fix a mistake: change the text in `dataN.js`, rebuild the HTML, and run `build_pdf.py` again.
