from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

SPRITE_SIZE = 64
BASE_SIZE = 16
OUT_DIR = Path(__file__).parent / "static" / "sprites"


def _blank() -> Image.Image:
    return Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))


def _resize(image: Image.Image) -> Image.Image:
    return image.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)


def render_battery() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(2, 10), (8, 7), (14, 10), (8, 13)], fill="#223347")
    draw.polygon([(2, 9), (8, 6), (14, 9), (8, 12)], fill="#3f5f7f")
    draw.polygon([(2, 9), (2, 10), (8, 13), (8, 12)], fill="#2f455d")
    draw.polygon([(8, 12), (8, 13), (14, 10), (14, 9)], fill="#354e68")
    draw.polygon([(8, 3), (10, 6), (8, 7), (6, 6)], fill="#ffd76a")
    draw.polygon([(8, 4), (9, 6), (8, 6), (7, 6)], fill="#fff0b8")
    draw.line((3, 10, 13, 10), fill="#2e445a")
    return _resize(image)


def render_city() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(1, 12), (8, 9), (14, 12), (8, 15)], fill="#112033")
    draw.polygon([(1, 11), (8, 8), (14, 11), (8, 14)], fill="#1d3556")
    draw.polygon([(1, 11), (1, 7), (8, 4), (8, 8)], fill="#2e4f74")
    draw.polygon([(8, 8), (8, 4), (14, 7), (14, 11)], fill="#274665")
    draw.polygon([(6, 8), (8, 7), (10, 8), (8, 9)], fill="#3d638f")
    for px, py in ((5, 9), (7, 8), (9, 9), (11, 10), (4, 10), (10, 11)):
        draw.point((px, py), fill="#ffd56e")
    draw.line((1, 11, 8, 8), fill="#5f84ae")
    draw.line((8, 8, 14, 11), fill="#4d6f97")
    return _resize(image)


def render_city_destroyed() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(1, 11), (8, 8), (14, 11), (8, 14)], fill="#3b242c")
    draw.polygon([(1, 11), (1, 8), (8, 5), (8, 8)], fill="#5a3438")
    draw.polygon([(8, 8), (8, 5), (14, 8), (14, 11)], fill="#4b2d33")
    draw.line((4, 7, 6, 10), fill="#ff8f5c")
    draw.line((10, 7, 12, 10), fill="#ff8f5c")
    draw.point((5, 8), fill="#ffd571")
    draw.point((10, 9), fill="#ffd571")
    return _resize(image)


def render_cursor() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    color = "#7be8ff"
    draw.line((8, 2, 8, 13), fill=color)
    draw.line((2, 8, 13, 8), fill=color)
    draw.rectangle((6, 6, 10, 10), outline="#dff9ff")
    return _resize(image)


def render_drone() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(8, 3), (3, 8), (8, 11), (13, 8)], fill="#ff7070")
    draw.polygon([(8, 5), (5, 8), (8, 10), (11, 8)], fill="#e35d5d")
    draw.line((4, 8, 12, 8), fill="#ffa0a0")
    draw.point((8, 12), fill="#ffd25f")
    return _resize(image)


def render_a10() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [(1, 10), (4, 8), (6, 8), (8, 6), (11, 6), (13, 5), (14, 6), (12, 8), (15, 9), (15, 10), (11, 10), (9, 12), (7, 12), (6, 10)],
        fill="#c4d2e5",
    )
    draw.line((4, 9, 12, 9), fill="#8da1be")
    draw.point((12, 6), fill="#7fc3ff")
    draw.point((5, 9), fill="#e8eff8")
    draw.point((10, 10), fill="#e8eff8")
    return _resize(image)


def render_missile() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(8, 2), (9, 4), (9, 12), (7, 12), (7, 4)], fill="#ffe89c")
    draw.polygon([(8, 1), (9, 3), (7, 3)], fill="#fff6cc")
    return _resize(image)


def render_ground() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 9), (8, 5), (15, 9), (8, 13)], fill="#3a5036")
    draw.polygon([(0, 9), (0, 10), (8, 14), (8, 13)], fill="#2d402a")
    draw.polygon([(8, 13), (8, 14), (15, 10), (15, 9)], fill="#324b2f")
    draw.line((1, 9, 8, 6), fill="#5e8e54")
    draw.line((8, 6, 14, 9), fill="#5e8e54")
    draw.point((8, 10), fill="#89a96f")
    draw.point((6, 10), fill="#78975f")
    draw.point((10, 10), fill="#78975f")
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
    inner = max(1, size // 2)
    draw.ellipse((center - inner, center - inner, center + inner, center + inner), fill="#fff5cf")
    for px, py in ((8, 8), (6, 8), (10, 8), (8, 6), (8, 10)):
        draw.point((px, py), fill="#fffdf0")
    return _resize(image)


def render_tehran_far() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 15, 15), fill="#0b1430")
    points = [(0, 10), (2, 9), (4, 8), (6, 9), (8, 7), (10, 8), (12, 7), (15, 9), (15, 15), (0, 15)]
    draw.polygon(points, fill="#182544")
    for x in range(0, 16, 5):
        draw.point((x + 1, 3 + (x % 2)), fill="#9cbcff")
    draw.line((0, 10, 15, 10), fill="#1f325d")
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
    draw.line((0, 10, 15, 10), fill="#3d6694")
    for x in (0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 14):
        for y in (11, 13):
            draw.point((x, y), fill="#ffd36f")
    return _resize(image)


SPRITES = {
    "a10": render_a10,
    "battery": render_battery,
    "city": render_city,
    "city_destroyed": render_city_destroyed,
    "cursor": render_cursor,
    "drone": render_drone,
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
