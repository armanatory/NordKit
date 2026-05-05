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
import textwrap


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


def render_slide(title, body, slide_number=None):
    """Render a single slide as a PIL Image."""
    img = Image.new("RGB", (SLIDE_WIDTH, SLIDE_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts
    title_font = load_font("LiberationSans-Regular.ttf", TITLE_FONT_SIZE)
    body_font = load_font("LiberationSans-Regular.ttf", BODY_FONT_SIZE)

    # Calculate layout
    x = PADDING
    y = PADDING
    max_width = SLIDE_WIDTH - 2 * PADDING

    # Draw title
    if title:
        title_lines = textwrap.wrap(title, width=25)
        for line in title_lines:
            draw.text((x, y), line, fill=TEXT_COLOR, font=title_font)
            y += int(TITLE_FONT_SIZE * LINE_SPACING)
        y += PADDING // 2

    # Draw body
    if body:
        body_lines = textwrap.wrap(body, width=35)
        for line in body_lines:
            draw.text((x, y), line, fill=TEXT_COLOR, font=body_font)
            y += int(BODY_FONT_SIZE * LINE_SPACING)
            if y > SLIDE_HEIGHT - PADDING - BODY_FONT_SIZE:
                break

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
