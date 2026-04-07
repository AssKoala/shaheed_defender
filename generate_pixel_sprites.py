from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SPRITE_SIZE = 64
BASE_SIZE = 16
OUT_DIR = Path(__file__).parent / "static" / "sprites"

SPRITES = {
    "battery": {"glyph": "^", "fg": "#ffd34d"},
    "city": {"glyph": "#", "fg": "#64e5ff"},
    "city_destroyed": {"glyph": "X", "fg": "#ff6b6b"},
    "cursor": {"glyph": "+", "fg": "#6ae6ff"},
    "drone": {"glyph": "V", "fg": "#ff5f5f"},
    "explosion_1": {"glyph": ".", "fg": "#fff3a1"},
    "explosion_2": {"glyph": "*", "fg": "#ffd166"},
    "explosion_3": {"glyph": "o", "fg": "#ffb347"},
    "explosion_4": {"glyph": "O", "fg": "#ff9248"},
    "explosion_5": {"glyph": "@", "fg": "#ff6b35"},
    "ground": {"glyph": "_", "fg": "#58b368"},
    "missile": {"glyph": "|", "fg": "#ffe680"},
    "star": {"glyph": ".", "fg": "#c8e6ff"},
}


def render_sprite(glyph: str, fg: str) -> Image.Image:
    font = ImageFont.load_default()
    image = Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), glyph, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = (BASE_SIZE - width) // 2 - bbox[0]
    y = (BASE_SIZE - height) // 2 - bbox[1]
    draw.text((x, y), glyph, font=font, fill=fg)
    return image.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, spec in SPRITES.items():
        sprite = render_sprite(spec["glyph"], spec["fg"])
        sprite.save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(SPRITES)} sprites to {OUT_DIR}")


if __name__ == "__main__":
    main()