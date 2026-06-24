# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-page static website for **정품사역** (Jeonpum Ministry), the mental health care ministry of Onnuri Church (온누리교회). There is no build system, no package manager, and no framework — the entire site is `index.html` with a single image asset `hero-bg.png`.

## Development

To preview locally, serve the root directory with any static HTTP server:

```bash
python3 -m http.server 8080
# or
npx serve .
```

There are no tests, no linting steps, and no compilation. Edit `index.html` directly.

## Architecture

Everything lives inside `index.html`:

- **CSS** — in a `<style>` block in `<head>`. All colors are CSS custom properties on `:root` (e.g. `--green-deep`, `--gold`, `--cream`). Responsive breakpoints at 768px and 480px.
- **HTML** — sections in order: top bar → nav → hero → greeting → about → checklist modal → about-detail modal → guide → apply → board → guide-card modals → emergency → team → footer.
- **JavaScript** — two inline `<script>` blocks and inline event handlers:
  1. Navigation toggle (`toggleMenu`, `closeMenu`) and board tab filtering (`filterBoard`).
  2. Guide card modal system: a `DISEASES` object keyed by Korean disease names (e.g. `'조현병'`, `'우울장애'`) drives the `openModal(key)` function that populates 4 tabs (질환 이해, 관찰 신호, 돌봄 지침, 즉각 연락). A separate `openAboutModal` / `closeAboutModal` pair controls the ministry-overview modal. The checklist modal (`openChecklist`, `runChecklist`, `resetChecklist`) uses `data-score` attributes on checkboxes to compute a risk score.
  3. Scroll-based fade-in via `IntersectionObserver` on elements with class `reveal`.

## Key Conventions

- **Language**: All user-visible content is Korean. Use Korean for any new copy.
- **Color palette**: Only use the CSS variables defined in `:root` — do not introduce raw hex values. The palette is extracted from `hero-bg.png` (forest greens, gold/brass tones, warm cream).
- **No external dependencies**: No CDN links, no npm packages. Keep it self-contained.
- **Inline event handlers**: The codebase uses `onclick=` attributes throughout. New interactive elements should follow this pattern rather than introducing `addEventListener` calls.
- **Board items**: Each `.board-item` carries a `data-cat` attribute matching one of the tab labels (`공지`, `프로그램`, `예배`, `스쿨`). New board entries must include this attribute for filtering to work.
- **Guide card modals**: To add a new disease card, add an entry to the `DISEASES` JS object and a corresponding `.guide-card` div with `onclick="openModal('키이름')"`.
- **Consultation form**: The "신청서 열기" button links to a Google Form URL. Update only that `href` if the form changes — the rest of the apply section is static.
