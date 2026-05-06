# NordKit Web App

A self-contained web application for creating and downloading Instagram Story slides (1080×1920 px).

## Features

- **Live Preview**: As you type, see your slide rendered at full resolution (visually scaled for display)
- **Pixel-Perfect Text Wrapping**: Text lines are wrapped based on actual pixel width, not character count
- **Markdown Support**: 
  - `**bold text**` for emphasis
  - `*italic text*` for styling
  - `- bullet point` for lists
- **Vertical Centering**: Content is automatically centered vertically for visual balance
- **Offline-First**: No external dependencies, no network requests—runs entirely in your browser
- **One-Click Export**: Download slides as 1080×1920 PNG files

## Usage

### Opening Locally

1. Navigate to the `web/` directory
2. Open `index.html` in any modern web browser:
   - **macOS/Linux**: `open index.html` or double-click
   - **Windows**: Double-click or right-click → Open with → Browser
   - **Command line**: `python3 -m http.server 8000` then visit `http://localhost:8000/`

### Creating a Slide

1. **Title** (optional): Enter the slide title in the "Title" field
2. **Body**: Enter the slide content in the "Body Text" area
3. **Preview**: The preview pane updates live as you type
4. **Download**: Click "Download PNG (1080×1920)" to save the slide as a PNG file

### Text Formatting

- **Bold**: Wrap text in double asterisks: `**important**`
- **Italic**: Wrap text in single asterisks: `*emphasis*`
- **Bullets**: Start a line with `- ` (dash + space)

Example:
```
This is a slide about **key concepts**:
- First point with *italics*
- Second point: **bold and emphasized**
- Final thought
```

## Technical Details

### Architecture

- **Single HTML file** (`index.html`) with embedded CSS and JavaScript
- **Canvas-based rendering**: Uses HTML5 `<canvas>` API to render slides at native 1080×1920 resolution
- **No build step**: Open `index.html` directly in a browser; no npm, webpack, or build tools needed
- **Offline**: All fonts, assets, and logic are local; no external API calls or CDN dependencies

### Font

- Uses the vendored **LiberationSans-Regular.ttf** (located in `../fonts/`)
- Falls back to system sans-serif fonts if the TTF cannot be loaded
- Font size: 60px for titles, 36px for body text

### Canvas API

- **Resolution**: 1080×1920 pixels (full Instagram Story resolution)
- **Text wrapping**: Uses `canvas.ctx.measureText()` to wrap based on actual pixel width
- **Export**: Uses `canvas.toBlob()` to generate PNG at native resolution
- **PNG generation** works in all modern browsers (Chrome, Firefox, Safari, Edge)

### Rendering Logic

The rendering process mirrors the Python CLI (`src/render.py`):

1. **First Pass**: Measure text to calculate total content height
2. **Centering**: Calculate vertical offset to center content within available space
3. **Second Pass**: Render title, body text, bullets, and markdown formatting
4. **Truncation Guard**: Lines that exceed the canvas boundary are not drawn; a warning is logged

This two-pass approach ensures content is properly centered while respecting canvas boundaries.

## Browser Compatibility

- **Chrome/Chromium** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

All modern browsers with HTML5 Canvas and `canvas.toBlob()` support.

## Offline & File-Based Deployment

The app is designed to work offline:

```bash
# Option 1: Open directly in browser
open index.html

# Option 2: Serve locally with Python
cd web/
python3 -m http.server 8000
# Then visit http://localhost:8000/

# Option 3: Serve with Node.js
npx http-server
```

There are no `fetch()` calls, no XHR requests, and no external dependencies. The app works from `file://` URLs as well as HTTP/HTTPS.

## Deployment

To deploy to a web server:

1. Copy the entire `web/` directory to your server
2. Serve `index.html` (and the colocated `LiberationSans-Regular.ttf`) over HTTP(S)
3. Ensure the web server is configured to serve `.ttf` files with the correct MIME type (`font/ttf` or `application/x-font-ttf`)

Example nginx config:
```nginx
location /web/ {
    types {
        font/ttf  ttf;
    }
    expires 7d;
}
```

## Non-Goals (Deliberately Out of Scope)

- Color picker or theme customization
- Image upload or background images
- Font family selector
- Markdown parsing beyond basic `**bold**` and `*italic*`
- Slide reordering or undo/redo
- AI-assisted narrative drafting
- Thumbnail strip preview

These are intentionally excluded to keep the app simple and offline-capable.

## Troubleshooting

### Canvas preview is blank
- Ensure JavaScript is enabled in your browser
- Check browser console for errors (F12 → Console tab)
- Try refreshing the page

### Font looks different than expected
- The browser is falling back to system sans-serif fonts
- This occurs if the TTF file is not loaded (common with `file://` URLs on some browsers)
- Workaround: Use a local HTTP server (`python3 -m http.server 8000`) instead

### PNG download is not working
- Check browser console for errors
- Ensure `canvas.toBlob()` is supported (all modern browsers support this)
- Try a different browser

### Text is cut off or wraps unexpectedly
- Verify your text doesn't exceed the available width (text is constrained to 1080px width − 120px padding)
- Remember that bold text uses a slightly larger font size, which may affect wrapping
- Long words without spaces may overflow; add soft hyphens (`­`) if needed

## Related Files

- **CLI renderer** (`../src/render.py`): Python backend; processes Markdown and renders slides
- **Font** (`../fonts/LiberationSans-Regular.ttf`): Vendored TrueType font used for rendering
- **Samples** (`../samples/example.md`): Example input for the CLI renderer

## License

See `../LICENSE` (or root `LICENSE` file) for licensing information.
