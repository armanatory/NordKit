#!/usr/bin/env python3
"""
NordKit CLI: Convert Markdown slides to 1080x1920 PNG files.

Usage:
    python render.py INPUT_FILE [-o OUTPUT_DIR]

Input: Markdown file with slides separated by '---'
Each slide has:
    # Title
    Body text...

Output: Numbered PNG files (01.png, 02.png, ...) in OUTPUT_DIR
"""

import sys
import os
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# Configuration
SLIDE_WIDTH = 1080
SLIDE_HEIGHT = 1920
BACKGROUND_COLOR = "#1a1a1a"
TEXT_COLOR = "#ffffff"
PADDING = 60
TITLE_FONT_SIZE = 60
BODY_FONT_SIZE = 36
LINE_SPACING = 1.5


def load_font(font_name, size):
    """Load a TrueType font from the fonts directory."""
    font_path = Path(__file__).parent.parent / "fonts" / font_name
    if not font_path.exists():
        raise FileNotFoundError(f"Font not found: {font_path}")
    try:
        return ImageFont.truetype(str(font_path), size)
    except Exception as e:
        raise RuntimeError(f"Failed to load font {font_path}: {e}")


def wrap_text_by_pixels(text, font, max_width):
    """Wrap text by pixel width using font.getlength(), not character count."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        line_width = font.getlength(test_line)

        if line_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines


def parse_markdown_line(text):
    """Parse markdown formatting: **bold**, *italic*, and return styled segments.

    Returns a list of (text, is_bold, is_italic) tuples.
    """
    segments = []
    i = 0
    current_text = ""
    current_bold = False
    current_italic = False

    while i < len(text):
        # Check for **bold**
        if i < len(text) - 1 and text[i:i+2] == "**":
            if current_text:
                segments.append((current_text, current_bold, current_italic))
                current_text = ""
            current_bold = not current_bold
            i += 2
        # Check for *italic* (but not **)
        elif text[i] == "*" and (i == 0 or text[i-1] != "*") and (i+1 >= len(text) or text[i+1] != "*"):
            if current_text:
                segments.append((current_text, current_bold, current_italic))
                current_text = ""
            current_italic = not current_italic
            i += 1
        else:
            current_text += text[i]
            i += 1

    if current_text:
        segments.append((current_text, current_bold, current_italic))

    return segments


def parse_body_text(body):
    """Parse body text into lines, handling bullets and markdown.

    Returns a list of (line_text, is_bullet, segments) tuples.
    Line text includes markdown formatting info in segments.
    """
    lines = []
    for line in body.split("\n"):
        line = line.rstrip()
        is_bullet = False

        if line.startswith("- "):
            is_bullet = True
            line = line[2:]

        segments = parse_markdown_line(line)
        lines.append((line, is_bullet, segments))

    return lines


def parse_slides(content):
    """Parse Markdown content into slides separated by '---'."""
    slides = []
    raw_slides = content.split("\n---\n")
    for raw_slide in raw_slides:
        raw_slide = raw_slide.strip()
        if not raw_slide:
            continue

        lines = raw_slide.split("\n", 1)
        title = lines[0].strip().lstrip("# ").strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        if title or body:
            slides.append({"title": title, "body": body})

    return slides


def draw_text_with_markdown(draw, x, y, text, font, color, max_width):
    """Draw text with markdown formatting support.

    Returns the y position after the drawn text.
    """
    segments = parse_markdown_line(text)
    current_x = x

    for segment_text, is_bold, is_italic in segments:
        if is_bold:
            bold_font = load_font("LiberationSans-Regular.ttf", int(font.size * 1.2))
            draw.text((current_x, y), segment_text, fill=color, font=bold_font)
            current_x += bold_font.getlength(segment_text)
        else:
            draw.text((current_x, y), segment_text, fill=color, font=font)
            current_x += font.getlength(segment_text)

    return current_x


def render_slide(title, body, slide_number=None):
    """Render a single slide as a PIL Image."""
    img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts
    title_font = load_font("LiberationSans-Regular.ttf", TITLE_FONT_SIZE)
    body_font = load_font("LiberationSans-Regular.ttf", BODY_FONT_SIZE)

    # Calculate available dimensions for content
    x = PADDING
    max_width = SLIDE_WIDTH - 2 * PADDING
    available_height = SLIDE_HEIGHT - 2 * PADDING - 60

    # First pass: measure content to enable vertical centering
    content_height = 0
    title_wrapped_lines = []
    body_wrapped_lines = []

    if title:
        title_wrapped_lines = wrap_text_by_pixels(title, title_font, max_width)
        content_height += len(title_wrapped_lines) * int(TITLE_FONT_SIZE * LINE_SPACING)
        content_height += PADDING // 2

    if body:
        body_lines = parse_body_text(body)
        for line_text, is_bullet, segments in body_lines:
            wrapped = wrap_text_by_pixels(line_text, body_font, max_width - (40 if is_bullet else 0))
            body_wrapped_lines.append((wrapped, is_bullet))
            content_height += len(wrapped) * int(BODY_FONT_SIZE * LINE_SPACING)

    # Calculate starting y to center content vertically
    y = PADDING + max(0, (available_height - content_height) // 2)

    # Draw title
    if title:
        for line in title_wrapped_lines:
            draw.text((x, y), line, fill=TEXT_COLOR, font=title_font)
            y += int(TITLE_FONT_SIZE * LINE_SPACING)
        y += PADDING // 2

    # Draw body
    if body:
        chars_lost = 0
        truncated = False
        for wrapped_lines, is_bullet in body_wrapped_lines:
            for wrapped_line in wrapped_lines:
                if y + int(BODY_FONT_SIZE * LINE_SPACING) > SLIDE_HEIGHT - PADDING:
                    chars_lost += len(wrapped_line)
                    truncated = True
                    continue

                # Draw bullet if needed
                if is_bullet:
                    bullet = "•"
                    draw.text((x + 20, y), bullet, fill=TEXT_COLOR, font=body_font)

                # Draw the actual text
                draw.text((x + (40 if is_bullet else 0), y), wrapped_line, fill=TEXT_COLOR, font=body_font)
                y += int(BODY_FONT_SIZE * LINE_SPACING)

        if truncated and chars_lost > 0:
            print(f"Warning: {chars_lost} characters truncated on slide", file=sys.stderr)

    # Draw slide number in bottom-right corner
    if slide_number is not None:
        slide_num_font = load_font("LiberationSans-Regular.ttf", 28)
        slide_num_text = str(slide_number).zfill(2)
        bbox = draw.textbbox((0, 0), slide_num_text, font=slide_num_font)
        num_width = bbox[2] - bbox[0]
        num_height = bbox[3] - bbox[1]
        num_x = SLIDE_WIDTH - PADDING - num_width
        num_y = SLIDE_HEIGHT - PADDING - num_height
        draw.text((num_x, num_y), slide_num_text, fill=TEXT_COLOR, font=slide_num_font)

    return img


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown slides to numbered PNG files."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to input Markdown file",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="slides",
        help="Output directory (default: slides/)",
    )

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Read input
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse slides
    slides = parse_slides(content)
    if not slides:
        print("Error: No slides found in input file", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}", file=sys.stderr)
        sys.exit(1)

    # Render and save slides
    try:
        for i, slide in enumerate(slides, start=1):
            print(f"Rendering slide {i}/{len(slides)}...", file=sys.stderr)
            img = render_slide(slide["title"], slide["body"], slide_number=i)
            output_path = output_dir / f"{i:02d}.png"
            img.save(output_path, "PNG")

        print(f"✓ Rendered {len(slides)} slides to {output_dir}/", file=sys.stderr)
    except Exception as e:
        print(f"Error rendering slides: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
