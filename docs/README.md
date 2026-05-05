# NordKit CLI — Text to Instagram Story Slides

A minimal command-line tool to convert Markdown text files into numbered 1080×1920 PNG slides, ready for Instagram story upload.

## Quick Start

### Installation

Prerequisites:
- Python 3.7+
- Pillow (`pip install Pillow`)

### Run the Example

```bash
python src/render.py samples/example.md
```

Output: PNG files numbered `01.png`, `02.png`, etc. in `slides/` directory.

### Verify the Output

```bash
ls -lah slides/
file slides/01.png  # Should be "image data, PNG"
```

## Usage

```bash
python src/render.py INPUT_FILE [-o OUTPUT_DIR]
```

### Arguments

- `INPUT_FILE` — Path to a Markdown file with slides separated by `---`
- `-o OUTPUT_DIR` — Output directory (default: `slides/`)

### Input Format

Create a Markdown file with slides separated by `---`:

```markdown
# Slide Title
Body text for the slide.

---

# Second Slide
More content here.
```

Each slide:
- **Title**: First line, starts with `#`
- **Body**: Remaining lines (auto-wrapped to fit the slide)
- **Separator**: `---` on its own line (blank lines before/after OK)

## Output

- **Format**: PNG (1080×1920 pixels, portrait)
- **Location**: `slides/` by default (or specified with `-o`)
- **Naming**: `01.png`, `02.png`, `03.png`, …
- **Theme**: Dark background (#1a1a1a) with light text (#ffffff)
- **Fonts**: LiberationSans (bundled in `fonts/`)

Each slide includes:
- Title (60pt font)
- Body (36pt font, auto-wrapped)
- Slide number in bottom-right corner (28pt font)

## Customization (Cycle 2+)

Currently, the tool ships with one built-in style (dark theme, LiberationSans). Future versions will support:
- Custom colors and themes
- Font selection
- Per-slide custom layouts
- Image support

For now, edit `src/render.py` directly to adjust colors, fonts, or spacing:
- `BACKGROUND_COLOR`: Background hex color
- `TEXT_COLOR`: Text hex color
- `TITLE_FONT_SIZE`, `BODY_FONT_SIZE`: Font sizes in pixels
- `PADDING`: Space around edges and between elements

## Troubleshooting

### "Font not found: `LiberationSans-Regular.ttf`"

Make sure you're running from the repo root directory:

```bash
cd /path/to/nordkit
python src/render.py samples/example.md
```

### Text is cut off or overlapping

This is a known limitation in cycle 1. Very long body text may overflow. For now:
- Keep body text under ~10 lines per slide
- Use shorter lines or bullet points
- Break long sections into multiple slides

This will be addressed in cycle 2 with text truncation / ellipsis handling.

### PNG files are empty or invalid

Check that Pillow is installed correctly:

```bash
python -c "from PIL import Image; print('Pillow OK')"
```

If it fails, install Pillow:

```bash
pip install Pillow
```

## Known Limitations (Cycle 1)

- One theme only (dark background, light text)
- One font only (LiberationSans)
- No image or logo support
- No per-slide custom layouts
- Text may overflow on very long slides (see Troubleshooting)
- No animation or video support
- Manual IG upload (not direct API integration)

## Next Steps

- **Cycle 2**: Browser-based WYSIWYG editor, theme customization, image support
- **Cycle 3**: Direct IG API publishing, animated formats, preset templates

## License & Attribution

- **LiberationSans Font**: Metrowerks/IBM/Red Hat. Licensed under SIL Open Font License. See `fonts/LICENSE`.
- **NordKit**: Built by the AI Venture Studio.

---

Built in cycle 1 of NordKit. Questions? Check the task spec at `tasks/cycle-1-cli-renderer.md`.
