from __future__ import annotations

import random
from dataclasses import asdict, dataclass

W = 80
H = 26

BATTERY_X = W // 2
BATTERY_Y = H - 2

CITY_POSITIONS = [8, 18, 28, 52, 62, 72]


def make_skyline(
    seed: int, max_h: int
) -> tuple[list[tuple[int, int, int]], frozenset[tuple[int, int]]]:
    rng = random.Random(seed)
    buildings: list[tuple[int, int, int]] = []
    windows: set[tuple[int, int]] = set()
    x = 0
    while x < W:
        bw = rng.randint(2, 7)
        bh = rng.randint(2, max_h)
        buildings.append((x, bw, bh))
        for rfg in range(1, bh - 1):
            for col in range(x + 1, min(x + bw - 1, W)):
                if rng.random() < 0.20:
                    windows.add((col, rfg))
        x += bw + rng.randint(0, 2)
    return buildings, frozenset(windows)


SKY_FAR, _ = make_skyline(7331, 7)
SKY_NEAR, WIN_NEAR = make_skyline(1337, 14)


@dataclass
class Drone:
    x: float
    y: float
    vx: float
    vy: float
    alive: bool = True


@dataclass
class Missile:
    x: float
    y: float
    tx: int
    ty: int
    dx: float = 0.0
    dy: float = 0.0
    alive: bool = True

    def __post_init__(self) -> None:
        dist = max(1.0, ((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2) ** 0.5)
        spd = 1.4
        self.dx = (self.tx - self.x) / dist * spd
        self.dy = (self.ty - self.y) / dist * spd


@dataclass
class Explosion:
    x: int
    y: int
    r: int = 0
    max_r: int = 5
    shrinking: bool = False
    alive: bool = True
    _t: int = 0
    rate: int = 3

    def advance(self) -> None:
        self._t += 1
        if self._t < self.rate:
            return
        self._t = 0
        if not self.shrinking:
            self.r += 1
            if self.r >= self.max_r:
                self.shrinking = True
        else:
            self.r -= 1
            if self.r < 0:
                self.alive = False


@dataclass
class City:
    x: int
    alive: bool = True


class GameEngine:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.drones: list[Drone] = []
        self.missiles: list[Missile] = []
        self.explosions: list[Explosion] = []
        self.cities: list[City] = [City(x) for x in CITY_POSITIONS]
        self.cx: int = W // 2
        self.cy: int = H // 2
        self.score: int = 0
        self.wave: int = 1
        self.ammo: int = 30
        self.game_over: bool = False
        self.ticks: int = 0
        self.last_refill_wave: int = 1

    def move_cursor(self, dx: int, dy: int) -> None:
        self.cx = max(1, min(W - 2, self.cx + dx))
        self.cy = max(1, min(H - 3, self.cy + dy))

    def set_cursor(self, x: int, y: int) -> None:
        self.cx = max(1, min(W - 2, x))
        self.cy = max(1, min(H - 3, y))

    def fire(self) -> None:
        if self.game_over or self.ammo <= 0:
            return
        self.ammo -= 1
        self.missiles.append(
            Missile(x=float(BATTERY_X), y=float(BATTERY_Y), tx=self.cx, ty=self.cy)
        )

    def click_fire(self, x: int, y: int) -> None:
        self.set_cursor(x, y)
        self.fire()

    def _spawn(self) -> None:
        alive = [c for c in self.cities if c.alive]
        if not alive:
            return
        target = random.choice(alive)
        sx = random.uniform(4, W - 4)
        spd = 0.18 + self.wave * 0.025 + random.uniform(-0.02, 0.04)
        dist = max(1.0, ((target.x - sx) ** 2 + (H - 2) ** 2) ** 0.5)
        vx = (target.x - sx) / dist * spd + random.uniform(-0.03, 0.03)
        vy = (H - 2) / dist * spd
        self.drones.append(Drone(x=sx, y=0.0, vx=vx, vy=vy))

    def tick(self) -> None:
        if self.game_over:
            return
        self.ticks += 1

        interval = max(8, 45 - self.wave * 4)
        count = 1 + self.wave // 4
        if self.ticks % interval == 0:
            for _ in range(random.randint(1, count)):
                self._spawn()

        for missile in self.missiles:
            if not missile.alive:
                continue
            missile.x += missile.dx
            missile.y += missile.dy
            if ((missile.x - missile.tx) ** 2 + (missile.y - missile.ty) ** 2) ** 0.5 < 1.6:
                self.explosions.append(Explosion(x=missile.tx, y=missile.ty))
                missile.alive = False

        for explosion in self.explosions:
            if not explosion.alive:
                continue
            explosion.advance()
            for drone in self.drones:
                if not drone.alive:
                    continue
                if ((drone.x - explosion.x) ** 2 + (drone.y - explosion.y) ** 2) ** 0.5 <= explosion.r + 0.5:
                    drone.alive = False
                    self.score += 10

        new_wave = 1 + self.score // 150
        if new_wave > self.last_refill_wave:
            self.last_refill_wave = new_wave
            self.ammo = min(30, self.ammo + 5)
        self.wave = new_wave

        for drone in self.drones:
            if not drone.alive:
                continue
            drone.x += drone.vx
            drone.y += drone.vy
            if drone.y >= H - 2:
                for city in self.cities:
                    if city.alive and abs(drone.x - city.x) < 3.5:
                        city.alive = False
                        self.explosions.append(Explosion(x=int(drone.x), y=H - 2, max_r=4))
                        break
                drone.alive = False

        self.drones = [o for o in self.drones if o.alive]
        self.missiles = [o for o in self.missiles if o.alive]
        self.explosions = [o for o in self.explosions if o.alive]

        if not any(c.alive for c in self.cities):
            self.game_over = True

    def state(self) -> dict:
        return {
            "w": W,
            "h": H,
            "battery_x": BATTERY_X,
            "battery_y": BATTERY_Y,
            "cursor": {"x": self.cx, "y": self.cy},
            "score": self.score,
            "wave": self.wave,
            "ammo": self.ammo,
            "game_over": self.game_over,
            "ticks": self.ticks,
            "cities": [asdict(city) for city in self.cities],
            "drones": [asdict(drone) for drone in self.drones],
            "missiles": [asdict(missile) for missile in self.missiles],
            "explosions": [asdict(explosion) for explosion in self.explosions],
        }