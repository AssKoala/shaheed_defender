from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

SPRITE_SIZE = 128
BASE_SIZE = 32
OUT_DIR = Path(__file__).parent / "static" / "sprites"


def _blank() -> Image.Image:
    return Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))


def _resize(image: Image.Image) -> Image.Image:
    return image.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)


def _iso_tile(top: str, left: str, right: str, detail: str | None = None) -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(16, 2), (30, 10), (16, 18), (2, 10)], fill=top)
    draw.polygon([(2, 10), (16, 18), (16, 28), (2, 20)], fill=left)
    draw.polygon([(16, 18), (30, 10), (30, 20), (16, 28)], fill=right)
    if detail:
        for px, py in ((9, 8), (13, 11), (19, 8), (23, 11), (16, 6), (16, 12)):
            draw.point((px, py), fill=detail)
    return image


def render_terrain_grass_a() -> Image.Image:
    return _resize(_iso_tile("#5b8f53", "#3f6f3d", "#4a7d46", "#8ec57f"))


def render_terrain_grass_b() -> Image.Image:
    return _resize(_iso_tile("#648f48", "#446a37", "#4f7840", "#9fce88"))


def render_terrain_rock() -> Image.Image:
    return _resize(_iso_tile("#57606f", "#434c59", "#4f5866", "#8d97a8"))


def render_battery() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(6, 18), (16, 12), (26, 18), (16, 24)], fill="#3d4f66")
    draw.polygon([(6, 18), (16, 24), (16, 30), (6, 24)], fill="#2d3f54")
    draw.polygon([(16, 24), (26, 18), (26, 24), (16, 30)], fill="#34495f")
    draw.polygon([(14, 9), (18, 9), (20, 13), (16, 15), (12, 13)], fill="#f4c866")
    draw.rectangle((14, 5, 18, 9), fill="#ffe39b")
    draw.line((8, 19, 24, 19), fill="#5f7692")
    return _resize(image)


def render_city() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(3, 20), (16, 14), (29, 20), (16, 27)], fill="#1a304a")
    draw.polygon([(3, 20), (3, 10), (16, 4), (16, 14)], fill="#2d4f77")
    draw.polygon([(16, 14), (16, 4), (29, 10), (29, 20)], fill="#24486f")
    draw.polygon([(12, 14), (16, 12), (20, 14), (16, 16)], fill="#3d688f")
    for px, py in (
        (8, 17), (10, 18), (13, 16), (15, 17), (18, 17), (21, 18), (23, 16),
        (9, 20), (14, 20), (19, 20), (24, 20)
    ):
        draw.rectangle((px, py, px + 1, py + 1), fill="#ffd774")
    return _resize(image)


def render_city_destroyed() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(3, 20), (16, 14), (29, 20), (16, 27)], fill="#3f272f")
    draw.polygon([(3, 20), (3, 12), (16, 6), (16, 14)], fill="#5a363d")
    draw.polygon([(16, 14), (16, 6), (29, 12), (29, 20)], fill="#4d2f36")
    draw.line((9, 10, 13, 16), fill="#ff9a5f")
    draw.line((20, 10, 23, 16), fill="#ff9a5f")
    draw.point((12, 11), fill="#ffd27a")
    draw.point((21, 11), fill="#ffd27a")
    return _resize(image)


def render_cursor() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    color = "#7be8ff"
    draw.line((16, 3, 16, 28), fill=color, width=1)
    draw.line((3, 16, 28, 16), fill=color, width=1)
    draw.rectangle((12, 12, 20, 20), outline="#dff9ff")
    return _resize(image)


def render_drone() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(16, 6), (4, 14), (16, 22), (28, 14)], fill="#f26e6e")
    draw.polygon([(16, 9), (8, 14), (16, 19), (24, 14)], fill="#d95a5a")
    draw.line((8, 14, 24, 14), fill="#ffaaaa")
    draw.rectangle((15, 23, 17, 25), fill="#ffd55f")
    return _resize(image)


def render_a10() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [(1, 19), (6, 15), (10, 15), (14, 11), (21, 11), (27, 8), (30, 10), (25, 14), (31, 17), (31, 19), (23, 19), (18, 24), (12, 24), (9, 20)],
        fill="#c7d3e3",
    )
    draw.polygon([(2, 19), (10, 19), (10, 21), (2, 21)], fill="#97a8be")
    draw.polygon([(10, 19), (24, 19), (24, 21), (10, 21)], fill="#b1bfce")
    draw.point((25, 10), fill="#7ec5ff")
    draw.point((12, 18), fill="#f3f8ff")
    draw.point((19, 19), fill="#f3f8ff")
    return _resize(image)


def render_rocket(frame: int) -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.polygon([(4, 16), (11, 12), (22, 12), (28, 16), (22, 20), (11, 20)], fill="#d9dce3")
    draw.polygon([(4, 16), (11, 12), (11, 20)], fill="#b8c0cf")
    draw.polygon([(22, 12), (28, 16), (22, 20)], fill="#aab3c3")
    draw.rectangle((13, 14, 20, 18), fill="#7ab8ff")
    draw.polygon([(6, 14), (10, 14), (8, 11)], fill="#cc4455")
    draw.polygon([(6, 18), (10, 18), (8, 21)], fill="#cc4455")

    if frame == 1:
        flame = [(2, 16), (5, 14), (5, 18)]
        color = "#ffb35d"
        core = "#fff0b5"
    elif frame == 2:
        flame = [(1, 16), (5, 13), (5, 19)]
        color = "#ff9248"
        core = "#ffe2a0"
    else:
        flame = [(3, 16), (5, 15), (5, 17)]
        color = "#ffc36d"
        core = "#fff4ca"

    draw.polygon(flame, fill=color)
    draw.point((4, 16), fill=core)
    draw.point((3, 16), fill=core)
    return _resize(image)


def render_star() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.point((16, 16), fill="#f4f8ff")
    draw.point((15, 16), fill="#a8cbff")
    draw.point((17, 16), fill="#a8cbff")
    draw.point((16, 15), fill="#a8cbff")
    draw.point((16, 17), fill="#a8cbff")
    return _resize(image)


def render_moon() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.ellipse((6, 6, 23, 23), fill="#fff0b5")
    draw.ellipse((11, 6, 27, 23), fill=(0, 0, 0, 0))
    return _resize(image)


def render_explosion(radius: int) -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    center_x, center_y = 16, 16
    max_r = {1: 4.0, 2: 6.0, 3: 8.0, 4: 10.0, 5: 12.0}[radius]

    # Build a soft radial body with heat bands to make the explosion look fuller.
    for y in range(BASE_SIZE):
        for x in range(BASE_SIZE):
            dx = x - center_x
            dy = y - center_y
            d = (dx * dx + dy * dy) ** 0.5
            if d > max_r + 1.5:
                continue

            if d <= max_r * 0.32:
                color = (255, 249, 212, 255)
            elif d <= max_r * 0.56:
                color = (255, 216, 125, 245)
            elif d <= max_r * 0.82:
                color = (255, 157, 72, 232)
            elif d <= max_r:
                color = (255, 102, 38, 210)
            else:
                fade = max(0, int(120 - (d - max_r) * 80))
                color = (255, 82, 22, fade)

            image.putpixel((x, y), color)

    # Jagged shell and sparks for a PS2-era sprite-sheet punch.
    shell_points = {
        1: [(16, 10), (19, 11), (21, 13), (22, 16), (20, 19), (17, 21), (14, 21), (11, 19), (10, 16), (11, 13), (13, 11)],
        2: [(16, 8), (20, 9), (23, 12), (24, 16), (23, 20), (20, 23), (16, 24), (12, 23), (9, 20), (8, 16), (9, 12), (12, 9)],
        3: [(16, 7), (21, 8), (25, 11), (27, 16), (25, 21), (22, 24), (16, 26), (11, 24), (7, 21), (5, 16), (7, 11), (11, 8)],
        4: [(16, 6), (22, 7), (27, 10), (29, 16), (27, 22), (23, 26), (16, 28), (10, 26), (5, 22), (3, 16), (5, 10), (10, 7)],
        5: [(16, 5), (23, 6), (28, 9), (31, 16), (28, 23), (24, 28), (16, 30), (9, 28), (4, 23), (1, 16), (4, 9), (9, 6)],
    }
    draw.polygon(shell_points[radius], outline="#ffd88a")

    spark_sets = {
        1: [(22, 14), (10, 18), (18, 23), (14, 9)],
        2: [(24, 13), (8, 18), (20, 25), (13, 7), (25, 18)],
        3: [(26, 12), (7, 20), (21, 27), (11, 6), (27, 19), (16, 5)],
        4: [(28, 12), (6, 21), (23, 28), (10, 5), (29, 19), (16, 4), (4, 14)],
        5: [(30, 11), (5, 22), (24, 30), (9, 4), (30, 20), (16, 3), (3, 14), (27, 6)],
    }
    for px, py in spark_sets[radius]:
        if 0 <= px < BASE_SIZE and 0 <= py < BASE_SIZE:
            draw.point((px, py), fill="#fff4cc")
            if px + 1 < BASE_SIZE:
                draw.point((px + 1, py), fill="#ffb85f")

    return _resize(image)


def render_tehran_far() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), fill="#0b1430")
    points = [(0, 20), (5, 18), (9, 16), (13, 17), (17, 14), (21, 16), (25, 15), (31, 18), (31, 31), (0, 31)]
    draw.polygon(points, fill="#182544")
    for x in range(0, 32, 7):
        draw.point((x + 1, 7 + (x % 3)), fill="#9cbcff")
    draw.line((0, 20, 31, 20), fill="#1f325d")
    return _resize(image)


def render_tehran_near() -> Image.Image:
    image = _blank()
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0, 0))
    draw.rectangle((0, 20, 5, 31), fill="#1d3557")
    draw.rectangle((6, 16, 11, 31), fill="#25456b")
    draw.rectangle((12, 12, 17, 31), fill="#305781")
    draw.rectangle((18, 18, 22, 31), fill="#203c5d")
    draw.rectangle((23, 14, 31, 31), fill="#2c4d74")
    draw.rectangle((15, 2, 16, 12), fill="#8eb9ff")
    draw.rectangle((14, 12, 17, 13), fill="#8eb9ff")
    draw.line((0, 20, 31, 20), fill="#3d6694")
    for x in (1, 3, 7, 9, 13, 15, 19, 21, 24, 27, 29):
        for y in (22, 26):
            draw.rectangle((x, y, x + 1, y + 1), fill="#ffd36f")
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
    "moon": render_moon,
    "rocket_1": lambda: render_rocket(1),
    "rocket_2": lambda: render_rocket(2),
    "rocket_3": lambda: render_rocket(3),
    "star": render_star,
    "tehran_far": render_tehran_far,
    "tehran_near": render_tehran_near,
    "terrain_grass_a": render_terrain_grass_a,
    "terrain_grass_b": render_terrain_grass_b,
    "terrain_rock": render_terrain_rock,
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, render in SPRITES.items():
        sprite = render()
        sprite.save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(SPRITES)} sprites to {OUT_DIR}")


if __name__ == "__main__":
    main()
