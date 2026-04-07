"""
shaheed_command.py  —  Missile Command clone
Incoming: Shaheed-136 delta-wing drones. Defend your cities.

pip install textual
python shaheed_command.py

Controls:
  Arrow keys — move targeting cursor
  Space      — fire interceptor missile
  R          — restart (game over screen)
  Q          — quit
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual import events
from textual.widget import Widget
from textual.widgets import Footer
from rich.text import Text

from game_engine import (
    BATTERY_X,
    BATTERY_Y,
    H,
    SKY_FAR,
    SKY_NEAR,
    W,
    WIN_NEAR,
    GameEngine,
)

# ── game widget ───────────────────────────────────────────────────────────────

class GameBoard(Widget):

    can_focus = True

    def __init__(self) -> None:
        super().__init__()
        self.engine = GameEngine()
        self._reset()
        self._text = Text()

    # ── state ─────────────────────────────────────────────────────────────────

    def _reset(self) -> None:
        self.engine.reset()

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def render(self) -> Text:
        return self._text

    def on_mount(self) -> None:
        self.set_interval(1 / 20, self._tick)  # 20 fps

    # ── game loop ─────────────────────────────────────────────────────────────

    def _tick(self) -> None:
        self.engine.tick()
        self._draw()

    # ── rendering ─────────────────────────────────────────────────────────────

    def _draw(self) -> None:
        # char grid: (char, style_str)
        blank = (' ', '')
        grid: list[list[tuple[str, str]]] = [
            [blank] * W for _ in range(H)
        ]

        def put(px: float, py: float, glyph: str, color: str = '') -> None:
            ix, iy = int(px), int(py)
            if 0 <= ix < W and 0 <= iy < H:
                grid[iy][ix] = (glyph, color)

        # ── sky gradient / stars ──
        for y in range(H - 3):
            for x in range(0, W, 12 + y % 5):
                put(x + (y * 7) % 11, y, '·', 'bright_black')

        # ── backdrop: diffused city skyline ──
        # Far tier — very dark silhouettes, no windows (too distant)
        for bx, bw, bh in SKY_FAR:
            top_y = H - 2 - bh
            for row in range(max(0, top_y), H - 2):
                for col in range(bx, min(bx + bw, W)):
                    put(col, row, '▀' if row == top_y else '█', '#0e1b28')

        # Near tier — taller buildings with lit windows and antenna spires
        for bx, bw, bh in SKY_NEAR:
            top_y = H - 2 - bh
            for row in range(max(0, top_y), H - 2):
                rfg = H - 2 - row
                for col in range(bx, min(bx + bw, W)):
                    if (col, rfg) in WIN_NEAR:
                        win_color = '#b87020' if (col + rfg) % 3 else '#3a7aaa'
                        put(col, row, '▪', win_color)
                    elif row == top_y:
                        put(col, row, '▀', '#253d55')
                    else:
                        put(col, row, '█', '#162535')
            if bh >= 9 and top_y > 0:
                put(bx + bw // 2, top_y - 1, '╵', '#2a4060')

        # ── ground line ──
        for x in range(W):
            put(x, H - 1, '▄', 'dim green')

        # ── cities ──
        for city in self.engine.cities:
            if city.alive:
                put(city.x - 2, H - 2, '▐', 'bold cyan')
                put(city.x - 1, H - 2, '█', 'bold cyan')
                put(city.x,     H - 2, '█', 'bold cyan')
                put(city.x + 1, H - 2, '█', 'bold cyan')
                put(city.x + 2, H - 2, '▌', 'bold cyan')
                put(city.x,     H - 1, '╨', 'bold cyan')
            else:
                for dx in range(-2, 3):
                    put(city.x + dx, H - 2, '░', 'red')

        # ── battery ──
        put(BATTERY_X - 2, H - 2, '╔', 'yellow')
        put(BATTERY_X - 1, H - 2, '╤', 'yellow')
        put(BATTERY_X,     H - 2, '▲', 'bold bright_yellow')
        put(BATTERY_X + 1, H - 2, '╤', 'yellow')
        put(BATTERY_X + 2, H - 2, '╗', 'yellow')

        # ── explosions (draw before drones so drones appear on top) ──
        exp_chars = ['·', '∘', '○', '◎', '●']
        for exp in self.engine.explosions:
            for dy in range(-exp.r, exp.r + 1):
                for dx in range(-exp.r, exp.r + 1):
                    if dx * dx + dy * dy <= exp.r * exp.r:
                        idx = min(exp.r, len(exp_chars) - 1)
                        style = 'bright_yellow' if not exp.shrinking else 'yellow'
                        put(exp.x + dx, exp.y + dy, exp_chars[idx], style)
            put(exp.x, exp.y, '◉', 'bold white')

        # ── drones: <▼> delta wing shape ──
        for d in self.engine.drones:
            put(d.x - 1, d.y, '╲', 'bold red')
            put(d.x,     d.y, '▼', 'bold bright_red')
            put(d.x + 1, d.y, '╱', 'bold red')
            # exhaust plume
            put(d.x, d.y - 1, '⁘', 'dim yellow')

        # ── A-10 support aircraft ──
        for a10 in self.engine.a10s:
            wing_left = '╼' if a10.vx > 0 else '╾'
            wing_right = '╾' if a10.vx > 0 else '╼'
            put(a10.x - 1, a10.y, wing_left, 'bold bright_white')
            put(a10.x,     a10.y, 'A', 'bold white')
            put(a10.x + 1, a10.y, wing_right, 'bold bright_white')
            put(a10.x, a10.y + 1, '┴', 'bright_black')

        # ── player missiles ──
        for m in self.engine.missiles:
            put(m.x, m.y,     '│', 'bold bright_yellow')
            put(m.x, m.y - 1, '╵', 'yellow')

        # ── targeting cursor ──
        put(self.engine.cx - 1, self.engine.cy, '─', 'bright_cyan')
        put(self.engine.cx + 1, self.engine.cy, '─', 'bright_cyan')
        put(self.engine.cx, self.engine.cy - 1, '│', 'bright_cyan')
        put(self.engine.cx, self.engine.cy + 1, '│', 'bright_cyan')
        put(self.engine.cx, self.engine.cy,     '⊕', 'bold bright_cyan')

        # ── assemble Rich Text ──
        t = Text(no_wrap=True)
        for row in grid:
            for ch, st in row:
                t.append(ch, style=st) if st else t.append(ch)
            t.append('\n')

        # ── HUD ──
        if self.engine.game_over:
            t.append('\n')
            t.append('  ╔══════════════════════════════╗\n', style='bold red')
            t.append('  ║        GAME  OVER            ║\n', style='bold red')
            t.append(f'  ║  Final Score: {self.engine.score:<14}║\n', style='bold white')
            t.append(f'  ║  Waves survived: {self.engine.wave - 1:<10}║\n', style='bold white')
            t.append('  ╚══════════════════════════════╝\n', style='bold red')
            t.append('        [R] Restart   [Q] Quit', style='dim')
        else:
            lives = sum(1 for c in self.engine.cities if c.alive)
            ammo_bar = '█' * self.engine.ammo + '░' * (30 - self.engine.ammo)
            t.append(f'  Score: ', style='bold white')
            t.append(f'{self.engine.score:<6}', style='bold green')
            t.append(f'  Wave: ', style='bold white')
            t.append(f'{self.engine.wave:<3}', style='bold yellow')
            t.append(f'  Cities: ', style='bold white')
            t.append(f'{lives}/6  ', style='bold cyan')
            t.append(f'  Ammo[', style='bold white')
            t.append(ammo_bar[:15], style='bold green' if self.engine.ammo > 10 else 'bold red')
            t.append(']  ', style='bold white')
            t.append('[Arrows/Mouse] Aim  [Space/Click] Fire  [Q] Quit', style='dim')

        self._text = t
        self.refresh()

    # ── input ─────────────────────────────────────────────────────────────────

    @staticmethod
    def _grid_pos(ex: int, ey: int) -> tuple[int, int]:
        """Convert widget-relative mouse coords to clamped grid coords.
        Offsets: 1 col left-border + 1 col left-padding, 1 row top-border."""
        col = max(1, min(W - 2, ex - 2))
        row = max(1, min(H - 3, ey - 1))
        return col, row

    def on_mouse_move(self, event: events.MouseMove) -> None:
        x, y = self._grid_pos(event.x, event.y)
        self.engine.set_cursor(x, y)

    def on_click(self, event: events.Click) -> None:
        x, y = self._grid_pos(event.x, event.y)
        self.engine.click_fire(x, y)

    def move(self, dx: int, dy: int) -> None:
        self.engine.move_cursor(dx, dy)

    def fire(self) -> None:
        self.engine.fire()

    def restart(self) -> None:
        self._reset()
        self._draw()


# ── app ───────────────────────────────────────────────────────────────────────

class ShaheedCommand(App):

    CSS = """
    Screen {
        background: #000005;
    }
    GameBoard {
        height: 1fr;
        background: #000010;
        border: tall #001133;
        padding: 0 1;
    }
    Footer {
        background: #0a0a1a;
        color: #444466;
    }
    """

    TITLE = "SHAHEED COMMAND"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield GameBoard()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(GameBoard).focus()

    def on_key(self, event: events.Key) -> None:
        board = self.query_one(GameBoard)
        k = event.key
        if   k == "up":    board.move(0, -1)
        elif k == "down":  board.move(0,  1)
        elif k == "left":  board.move(-2, 0)
        elif k == "right": board.move( 2, 0)
        elif k == "space": board.fire()
        elif k == "r" and board.engine.game_over: board.restart()


if __name__ == "__main__":
    ShaheedCommand().run()