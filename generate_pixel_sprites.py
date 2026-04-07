from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SPRITE_SIZE = 64
BASE_SIZE = 16
OUT_DIR = Path(__file__).parent / "static" / "sprites"

def _blank() -> Image.Image:
    return Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))


def _resize(image: Image.Image) -> Image.Image:
    return image.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)


def render_ascii_sprite(glyph: str, fg: str) -> Image.Image:
    font = ImageFont.load_default()
    image = _blank()
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), glyph, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = (BASE_SIZE - width) // 2 - bbox[0]
    y = (BASE_SIZE - height) // 2 - bbox[1]
    draw.text((x, y), glyph, font=font, fill=fg)
    return _resize(image)


def render_city() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 10, 15, 15), fill="#081223")
    draw.rectangle((1, 9, 4, 15), fill="#213d63")
    draw.rectangle((5, 7, 9, 15), fill="#345a87")
    draw.rectangle((10, 8, 15, 15), fill="#27476f")
    draw.rectangle((7, 5, 8, 7), fill="#4f7db0")
    for x in (2, 3, 6, 7, 8, 11, 12, 13):
        for y in (10, 12, 14):
            draw.point((x, y), fill="#ffd776")
    return _resize(image)


def render_city_destroyed() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 11, 15, 15), fill="#160d12")
    draw.rectangle((1, 10, 5, 15), fill="#4a2a32")
    draw.rectangle((6, 8, 9, 15), fill="#5d3032")
    draw.rectangle((10, 11, 15, 15), fill="#3a1e28")
    draw.line((2, 7, 6, 11), fill="#ff8f5c", width=1)
    draw.line((10, 7, 13, 11), fill="#ff8f5c", width=1)
    draw.point((4, 8), fill="#ffcc66")
    draw.point((11, 8), fill="#ffcc66")
    return _resize(image)


def render_battery() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 11, 13, 15), fill="#284056")
    draw.rectangle((4, 9, 11, 11), fill="#415f79")
    draw.rectangle((7, 4, 9, 9), fill="#ffd34d")
    draw.rectangle((6, 3, 10, 4), fill="#ffe38a")
    return _resize(image)


def render_cursor() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    color = "#6ae6ff"
    draw.line((8, 2, 8, 13), fill=color, width=1)
    draw.line((2, 8, 13, 8), fill=color, width=1)
    draw.rectangle((6, 6, 10, 10), outline="#e6ffff")
    return _resize(image)


def render_drone() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(8, 4), (3, 8), (6, 10), (8, 9), (10, 10), (13, 8)], fill="#ff6b6b")
    draw.point((8, 11), fill="#ffc857")
    return _resize(image)


def render_a10() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [(2, 9), (5, 8), (6, 6), (9, 6), (12, 4), (13, 5), (11, 7), (14, 8), (14, 9), (10, 9), (8, 12), (7, 12), (6, 9)],
        fill="#c8d4e8",
    )
    draw.rectangle((4, 8, 11, 9), fill="#8aa2c2")
    draw.point((12, 5), fill="#7dc5ff")
    return _resize(image)


def render_missile() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((7, 3, 8, 13), fill="#ffe680")
    draw.point((7, 2), fill="#fff6b0")
    draw.point((8, 2), fill="#fff6b0")
    return _resize(image)


def render_ground() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 12, 15, 15), fill="#203226")
    draw.line((0, 11, 15, 11), fill="#4ca96b")
    return _resize(image)


def render_star() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.point((8, 8), fill="#f4f8ff")
    draw.point((7, 8), fill="#a8cbff")
    draw.point((9, 8), fill="#a8cbff")
    draw.point((8, 7), fill="#a8cbff")
    draw.point((8, 9), fill="#a8cbff")
    return _resize(image)


def render_moon() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 2, 11, 11), fill="#fff0b5")
    draw.ellipse((5, 2, 13, 11), fill=(0, 0, 0, 0))
    return _resize(image)


def render_explosion(radius: int) -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    colors = {
        1: "#fff2b0",
        2: "#ffd166",
        3: "#ffb347",
        4: "#ff9248",
        5: "#ff6b35",
    }
    size = 2 + radius * 2
    center = 8
    draw.ellipse((center - size, center - size, center + size, center + size), fill=colors[radius])
    draw.ellipse((center - max(1, size // 2), center - max(1, size // 2), center + max(1, size // 2), center + max(1, size // 2)), fill="#fff5cf")
    return _resize(image)


def render_tehran_far() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 15, 15), fill="#0b1430")
    points = [(0, 10), (2, 9), (4, 8), (6, 9), (8, 7), (10, 8), (12, 7), (15, 9), (15, 15), (0, 15)]
    draw.polygon(points, fill="#182544")
    for x in range(0, 16, 5):
        draw.point((x + 1, 3 + (x % 2)), fill="#9cbcff")
    return _resize(image)


def render_tehran_near() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 15, 15), fill=(0, 0, 0, 0))
    draw.rectangle((0, 10, 2, 15), fill="#1d3557")
    draw.rectangle((3, 8, 5, 15), fill="#25456b")
    draw.rectangle((6, 6, 8, 15), fill="#305781")
    draw.rectangle((9, 9, 11, 15), fill="#203c5d")
    draw.rectangle((12, 7, 15, 15), fill="#2c4d74")
    draw.rectangle((7, 1, 7, 6), fill="#8eb9ff")
    draw.rectangle((6, 6, 8, 6), fill="#8eb9ff")
    for x in (0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 14):
        for y in (11, 13):
            draw.point((x, y), fill="#ffd36f")
    return _resize(image)


SPRITES = {
    "battery": render_battery,
    "city": render_city,
    "city_destroyed": render_city_destroyed,
    "cursor": render_cursor,
    "drone": render_drone,
    "a10": render_a10,
    "explosion_1": lambda: render_explosion(1),
    "explosion_2": lambda: render_explosion(2),
    "explosion_3": lambda: render_explosion(3),
    "explosion_4": lambda: render_explosion(4),
    "explosion_5": lambda: render_explosion(5),
    "ground": render_ground,
    "missile": render_missile,
    "moon": render_moon,
    "star": render_star,
    "tehran_far": render_tehran_far,
    "tehran_near": render_tehran_near,
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, render in SPRITES.items():
        sprite = render()
        sprite.save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(SPRITES)} sprites to {OUT_DIR}")


if __name__ == "__main__":
    main()