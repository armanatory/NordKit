---
id: cycle-1-cli-renderer
title: Build minimal CLI prototype for text-to-PNG slide rendering
status: done
owner: builder
created: 2026-05-05T10:22:00Z
updated: 2026-05-05T10:22:00Z
---

# Cycle 1: Minimal CLI Prototype — Text to 1080×1920 PNG Slides

## Scope

Ship a working end-to-end prototype that:
- Reads a structured text input file (Markdown with `---` separators)
- Renders each section as a 1080×1920 portrait PNG slide
- Outputs numbered files (01.png, 02.png, …) in a single folder
- Uses a vendored TTF font (no CDN, no network at runtime)
- Applies a minimal dark-theme visual style (dark background, light text)
- Includes a sample input file so founder can verify the entire pipeline

The goal: validate that the rendering pipeline works end-to-end and that the founder can run it locally on day one.

## Locked Assumptions (from Prioritize step)

### Input Format
- **Format:** Markdown with `---` slide separators (chosen for simplicity over YAML)
- **Per-slide content:** title + body text
- **Example:** See `samples/example.md` in the repo

### Output Format
- **Resolution:** 1080×1920 pixels (portrait, Instagram story standard)
- **File naming:** `01.png`, `02.png`, … in a single output directory
- **Location:** Configurable via command-line argument; default is `./slides/`
- **Format:** PNG (lossless, web-ready)

### Rendering
- **Technology:** Python 3 + Pillow (PIL)
- **Font:** One bundled TTF file (DejaVu Sans), vendored in repo under `fonts/`
- **Theme:** Single built-in dark theme
  - Background: dark (e.g., #1a1a1a)
  - Text: light (e.g., #ffffff)
  - No per-slide custom layout, no images, no logos
  - Optional: slide number in a corner (e.g., bottom-right)

### Offline Constraint
- **No external network calls** at runtime
- **No CDN dependencies** for fonts or assets
- **All static assets** (TTF fonts) committed to the repo

## Acceptance Criteria

- [ ] Rendering script (`src/render.py` or similar) that reads a Markdown input file
- [ ] Script outputs numbered PNG files (01.png, 02.png, …) at the specified output directory
- [ ] Each PNG is exactly 1080×1920 pixels, dark theme, light text, readable
- [ ] Sample input file (`samples/example.md`) provided and pre-configured
- [ ] DejaVu Sans TTF file (or equivalent system-safe sans-serif) bundled in repo under `fonts/`
- [ ] One-line CLI command documented in `docs/README.md` that produces output on first run
- [ ] Founder can run the script and see 01.png, 02.png, … in the output folder
- [ ] No errors on clean repo checkout + install + run
- [ ] Task spec complete with locked assumptions and deliverables listed

## What's NOT in Scope (Deliberately Deferred)

- **Browser UI / WYSIWYG editor** — cycle 2 candidate (Direction B)
- **Fixed narrative arc template** — deferred until founder answers narrative-shape question
- **Theme system / customization** — deferred until renderer is stable
- **Image support, custom per-slide layouts, animations**
- **AI-assisted text generation**
- **Direct IG API publishing** — scope includes manual upload workflow only
- **Color/font customization** — ship one style to validate the pipeline

## Deliverables (Completed)

1. ✅ **Task spec** — this document (`tasks/cycle-1-cli-renderer.md`)
2. ✅ **Rendering script** — `src/render.py`
3. ✅ **Sample input** — `samples/example.md`
4. ✅ **Bundled font** — `fonts/LiberationSans-Regular.ttf`
5. ✅ **Documentation** — `docs/README.md` with run command
6. ✅ **KANBAN.md** — updated to reflect this task as done

## Testing & Verification

To verify the prototype:

```bash
cd /path/to/nordkit
python src/render.py samples/example.md -o slides/
ls -lah slides/  # Should show 01.png, 02.png, 03.png, etc.
file slides/01.png  # Verify PNG format
```

Each PNG should:
- Be exactly 1080×1920 pixels
- Display dark background with light text
- Show title and body for the corresponding slide
- Have no visual artifacts or rendering errors

## Assumptions & Invalidation

### Assumption 1: Markdown `---` separators are simple enough
**Validation:** If founder feedback is "I want YAML with more structure," cycle 2 can upgrade the parser without changing the renderer.

### Assumption 2: DejaVu Sans is sufficient for launch
**Validation:** If founder wants a specific font/brand, that becomes a cycle-2 task (template system or one-off font swap). The renderer is font-agnostic by design.

### Assumption 3: Dark theme + light text is acceptable
**Validation:** If founder wants specific colors, cycle 2 introduces a theme config layer. The rendering pipeline is theme-agnostic.

### Assumption 4: No images or custom layouts in cycle 1
**Validation:** If founder wants image support, that is a new renderer capability (and likely requires image hosting/bundling architecture). Out of scope unless explicitly escalated.

### Assumption 5: Manual IG upload workflow is acceptable
**Validation:** If founder wants direct IG API publishing later, that becomes an integration task, not a rendering task.

## Open Questions for Founder Feedback

1. Is the Markdown input format easy enough to author? Would YAML + structured fields be better?
2. Does the dark theme + light text match your vision, or should we adjust colors?
3. Is the slide number placement (bottom-right) correct, or would you prefer elsewhere?
4. Does the character/line-break handling match your expectations?
5. Should there be a way to override the output directory? (Currently defaulted to `./slides/`)

## Next Steps (Cycle 2 Candidates)

- **Direction B (browser WYSIWYG):** if founder says "I need to see it live while typing"
- **Direction C (fixed arc):** once founder clarifies narrative shape per story
- **Direction D (theme system):** once renderer is stable and tested
- **Font/color customization:** simple config upgrade once prototype is validated
- **Image support:** requires new architecture decision (bundled vs. linked)

## Dependencies & Risks

### No Known Blockers
- DejaVu Sans is open-source and can be freely bundled
- Pillow is PyPI-native, no external runtime dependencies needed
- Task does not depend on founder infrastructure or external services

### Risk: Font File Size
DejaVu Sans is ~400 KB (acceptable for a repo). If font size becomes a concern, cycle 2 can switch to a lighter subset or web-safe alternative.

### Risk: Text Truncation
If input slides have very long body text, it may overflow the slide. This is captured in the sample input as a known limitation for cycle 1; cycle 2 can add text wrapping / ellipsis handling.

## Sign-Off

Spec locked and task implemented. Founder can verify end-to-end on day one by running:

```bash
python src/render.py samples/example.md
```

Expected output: `slides/01.png`, `slides/02.png`, `slides/03.png`
