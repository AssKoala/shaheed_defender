from __future__ import annotations

import random
from dataclasses import asdict, dataclass

W = 80
H = 26

BATTERY_X = W - 10
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


@dataclass
class A10:
    x: float
    y: float
    vx: float
    alive: bool = True


class GameEngine:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.drones: list[Drone] = []
        self.missiles: list[Missile] = []
        self.explosions: list[Explosion] = []
        self.a10s: list[A10] = []
        self.cities: list[City] = [City(x) for x in CITY_POSITIONS]
        self.cx: int = W // 2
        self.cy: int = H // 2
        self.score: int = 0
        self.wave: int = 1
        self.ammo: int = 30
        self.game_over: bool = False
        self.ticks: int = 0
        self.last_refill_wave: int = 1
        self.last_a10_spawn: int = 0

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
        lane = random.choice(("left", "top_left", "top_right"))
        if lane == "left":
            sx = random.uniform(-4.0, 2.0)
            sy = random.uniform(3.0, H * 0.65)
        elif lane == "top_left":
            sx = random.uniform(2.0, W * 0.38)
            sy = random.uniform(-4.0, 1.0)
        else:
            sx = random.uniform(W * 0.62, W - 2.0)
            sy = random.uniform(-4.0, 1.0)
        spd = 0.18 + self.wave * 0.025 + random.uniform(-0.02, 0.04)
        tx = float(target.x)
        ty = float(H - 2)
        dist = max(1.0, ((tx - sx) ** 2 + (ty - sy) ** 2) ** 0.5)
        vx = (target.x - sx) / dist * spd + random.uniform(-0.03, 0.03)
        vy = (ty - sy) / dist * spd + random.uniform(-0.012, 0.012)
        self.drones.append(Drone(x=sx, y=sy, vx=vx, vy=vy))

    def _spawn_a10(self) -> None:
        if self.a10s:
            return
        x = W + 5.0
        y = H - random.uniform(5.2, 7.0)
        vx = -random.uniform(0.55, 0.75)
        self.a10s.append(A10(x=x, y=y, vx=vx))
        self.last_a10_spawn = self.ticks

    def _trigger_a10_strike(self) -> None:
        cleared = 0
        for drone in self.drones:
            if not drone.alive:
                continue
            drone.alive = False
            cleared += 1
            self.explosions.append(Explosion(x=int(drone.x), y=int(drone.y), max_r=3))
        if cleared:
            self.score += cleared * 10
        self.score += 50

    def tick(self) -> None:
        if self.game_over:
            return
        self.ticks += 1

        interval = max(8, 45 - self.wave * 4)
        count = 1 + self.wave // 4
        if self.ticks % interval == 0:
            for _ in range(random.randint(1, count)):
                self._spawn()

        a10_interval = max(220, 560 - self.wave * 20)
        if self.ticks - self.last_a10_spawn >= a10_interval:
            self._spawn_a10()

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
            for a10 in self.a10s:
                if not a10.alive:
                    continue
                if ((a10.x - explosion.x) ** 2 + (a10.y - explosion.y) ** 2) ** 0.5 <= explosion.r + 0.75:
                    a10.alive = False
                    self._trigger_a10_strike()

        new_wave = 1 + self.score // 150
        if new_wave > self.last_refill_wave:
            self.last_refill_wave = new_wave
            self.ammo = min(30, self.ammo + 5)
        self.wave = new_wave

        for a10 in self.a10s:
            if not a10.alive:
                continue
            a10.x += a10.vx
            a10.y += -0.055
            if a10.x < -6 or a10.x > W + 6:
                a10.alive = False

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
        self.a10s = [o for o in self.a10s if o.alive]

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
            "a10s": [asdict(a10) for a10 in self.a10s],
        }